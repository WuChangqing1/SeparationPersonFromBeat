#!/usr/bin/env python
"""
SeparationPersonFromBeat - CLI entry point.
人声与伴奏分离工具，基于 Meta Demucs.
"""

import argparse
from pathlib import Path

from .separator import separate


def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="separation",
        description="人声与伴奏分离工具 - 基于 Demucs 的音频源分离",
    )
    parser.add_argument(
        "-i", "--input",
        type=Path,
        required=True,
        help="输入音频文件路径",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("output"),
        help="输出目录 (默认: ./output)",
    )
    parser.add_argument(
        "-m", "--model",
        default="htdemucs",
        help="模型名称 (默认: htdemucs). 可选: htdemucs, htdemucs_ft, htdemucs_6s, mdx_extra",
    )
    parser.add_argument(
        "--device",
        default=None,
        help="设备: cuda 或 cpu (默认: 自动检测)",
    )
    parser.add_argument(
        "--shifts",
        type=int,
        default=1,
        help="等变稳定化的随机偏移次数 (默认: 1, 提高质量但增加耗时)",
    )
    parser.add_argument(
        "--overlap",
        type=float,
        default=0.25,
        help="分段之间的重叠比例 (默认: 0.25)",
    )
    parser.add_argument(
        "--two-stems",
        default=None,
        metavar="STEM",
        help="只分离为 {STEM} 和 no_{STEM} 两轨 (如: vocals)",
    )
    parser.add_argument(
        "--segment",
        type=int,
        default=None,
        help="每段的帧数，用于限制显存占用",
    )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    separate(
        input_path=args.input,
        output_dir=args.output,
        model_name=args.model,
        device=args.device,
        shifts=args.shifts,
        overlap=args.overlap,
        two_stems=args.two_stems,
        segment=args.segment,
    )


if __name__ == "__main__":
    main()
