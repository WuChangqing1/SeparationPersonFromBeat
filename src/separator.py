"""
Core separation engine using Demucs.
All Demucs calls go through this module, which enforces GPU readiness checks.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

import torch

from demucs.apply import apply_model, BagOfModels
from demucs.audio import save_audio
from demucs.pretrained import get_model_from_args, add_model_flags
from demucs.separate import load_track


def check_gpu() -> dict:
    """Verify GPU readiness and return status info.

    Must be called before any Demucs model loading.
    """
    info = {
        "pytorch_version": torch.__version__,
        "cuda_available": torch.cuda.is_available(),
    }
    if info["cuda_available"]:
        info["cuda_version"] = torch.version.cuda
        info["gpu_count"] = torch.cuda.device_count()
        info["gpu_name"] = torch.cuda.get_device_name(0)
    return info


def print_gpu_status(info: dict) -> None:
    """Print GPU status to console."""
    print("=" * 50)
    print("GPU STATUS CHECK")
    print("=" * 50)
    print(f"  PyTorch version : {info['pytorch_version']}")
    print(f"  CUDA available  : {info['cuda_available']}")
    if info["cuda_available"]:
        print(f"  CUDA version    : {info['cuda_version']}")
        print(f"  GPU count       : {info['gpu_count']}")
        print(f"  GPU name        : {info['gpu_name']}")
    else:
        print("  WARNING: GPU NOT available, will fall back to CPU (slow).")
    print("=" * 50)


def build_model_args(
    model_name: str = "htdemucs",
    repo: Optional[Path] = None,
) -> argparse.Namespace:
    """Build argparse.Namespace for demucs model loading."""
    parser = argparse.ArgumentParser()
    add_model_flags(parser)
    args = parser.parse_args([])
    args.name = model_name
    if repo is not None:
        args.repo = repo
    return args


def separate(
    input_path: Path,
    output_dir: Path,
    model_name: str = "htdemucs",
    device: Optional[str] = None,
    shifts: int = 1,
    overlap: float = 0.25,
    two_stems: Optional[str] = None,
    segment: Optional[int] = None,
) -> list[Path]:
    """Separate audio sources from a track.

    Returns list of output file paths.
    """
    # --- GPU check (BEFORE any Demucs call) ---
    gpu_info = check_gpu()
    print_gpu_status(gpu_info)

    # --- Resolve device ---
    if device is None:
        device = "cuda" if gpu_info["cuda_available"] else "cpu"

    print(f"\nUsing device: {device}")

    # --- Load model ---
    print(f"\nLoading model: {model_name} ...")
    args = build_model_args(model_name)
    model = get_model_from_args(args)
    model.to(device)
    model.eval()

    if isinstance(model, BagOfModels):
        print(f"Model is a bag of {len(model.models)} models.")
    print(f"Model sources: {model.sources}")
    print(f"Model samplerate: {model.samplerate} Hz")

    # --- Validate stems ---
    if two_stems is not None and two_stems not in model.sources:
        available = ", ".join(model.sources)
        print(f"ERROR: stem '{two_stems}' not found. Available: {available}")
        sys.exit(1)

    # --- Prepare output ---
    out = output_dir / model_name
    out.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {out.resolve()}")

    # --- Process track ---
    if not input_path.exists():
        print(f"ERROR: File not found: {input_path}")
        sys.exit(1)

    print(f"\nLoading track: {input_path}")
    wav = load_track(input_path, model.audio_channels, model.samplerate)

    # Normalize
    ref = wav.mean(0)
    wav = wav - ref.mean()
    wav = wav / ref.std()

    print(f"Separating sources (device={device}, shifts={shifts}, overlap={overlap})...")
    sources = apply_model(
        model,
        wav[None],
        device=device,
        shifts=shifts,
        split=True,
        overlap=overlap,
        progress=True,
        segment=segment,
    )[0]

    sources = sources * ref.std()
    sources = sources + ref.mean()

    # --- Save results ---
    output_files = []
    ext = "wav"
    kwargs = {
        "samplerate": model.samplerate,
        "clip": "rescale",
        "as_float": False,
        "bits_per_sample": 16,
    }

    if two_stems is None:
        for source, name in zip(sources, model.sources):
            stem = out / f"{input_path.stem}" / f"{name}.{ext}"
            stem.parent.mkdir(parents=True, exist_ok=True)
            save_audio(source, str(stem), **kwargs)
            output_files.append(stem)
            print(f"  Saved: {stem}")
    else:
        sources_list = list(sources)
        idx = model.sources.index(two_stems)
        stem = out / f"{input_path.stem}" / f"{two_stems}.{ext}"
        stem.parent.mkdir(parents=True, exist_ok=True)
        save_audio(sources_list.pop(idx), str(stem), **kwargs)
        output_files.append(stem)
        print(f"  Saved: {stem}")

        # Combine remaining sources into "no_{stem}"
        other = torch.zeros_like(sources_list[0])
        for s in sources_list:
            other += s
        other_stem = out / f"{input_path.stem}" / f"no_{two_stems}.{ext}"
        other_stem.parent.mkdir(parents=True, exist_ok=True)
        save_audio(other, str(other_stem), **kwargs)
        output_files.append(other_stem)
        print(f"  Saved: {other_stem}")

    print(f"\nDone. {len(output_files)} file(s) saved.")
    return output_files
