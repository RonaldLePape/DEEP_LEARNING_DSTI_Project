# split_plantvillage.py
import argparse, random, shutil
from pathlib import Path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True, help="Path to original PlantVillage root (class subfolders inside)")
    p.add_argument("--dst", required=True, help="Output root (will create train/val/test)")
    p.add_argument("--train", type=float, default=0.70, help="Train ratio (default 0.70)")
    p.add_argument("--val", type=float, default=0.10, help="Val ratio (default 0.10)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--copy", action="store_true", help="Copy files instead of symlink (default symlink on POSIX)")
    args = p.parse_args()

    assert 0 < args.train < 1 and 0 <= args.val < 1, "ratios must be in (0,1)"
    total = args.train + args.val
    assert abs(1.0 - (total + 0.20)) < 1e-6 or total <= 0.80 + 1e-9, \
        "You asked for train+val=80%; adjust --train/--val so they sum to 0.80 (e.g., 0.70/0.10)."
    test_ratio = 1.0 - (args.train + args.val)

    random.seed(args.seed)
    src = Path(args.src)
    dst = Path(args.dst)
    for split in ["train", "val", "test"]:
        (dst / split).mkdir(parents=True, exist_ok=True)

    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff"}
    classes = [d for d in src.iterdir() if d.is_dir()]
    classes.sort(key=lambda p: p.name.lower())

    def link_or_copy(src_path: Path, dst_path: Path):
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            if args.copy or (hasattr(shutil, "copy2") and dst.drive != src.drive):
                shutil.copy2(src_path, dst_path)
            else:
                # Prefer symlinks for speed/storage on same filesystem
                dst_path.symlink_to(src_path.resolve())
        except Exception:
            shutil.copy2(src_path, dst_path)

    for cls in classes:
        imgs = [p for p in cls.rglob("*") if p.suffix.lower() in exts and p.is_file()]
        imgs.sort()
        random.shuffle(imgs)

        n = len(imgs)
        n_train = int(args.train * n)
        n_val = int(args.val * n)
        n_test = n - n_train - n_val  # ensures total sum = n

        splits = {
            "train": imgs[:n_train],
            "val": imgs[n_train:n_train + n_val],
            "test": imgs[n_train + n_val:],
        }

        for split, files in splits.items():
            out_dir = dst / split / cls.name
            for f in files:
                link_or_copy(f, out_dir / f.name)

        print(f"{cls.name}: total={n} → train={n_train}, val={n_val}, test={n_test}")

    print("\nDone. Structure:")
    print(dst / "train")
    print(dst / "val")
    print(dst / "test")

if __name__ == "__main__":
    main()
