# Keyboard shortcuts helper for [kitty terminal](https://github.com/kovidgoyal/kitty)

This helper is a modified version of script I saw [here](https://github.com/Jakeroid/kitty-shortcuts-work-only-with-latin-characters)

Helps to bypass issues
* https://github.com/kovidgoyal/kitty/issues/606
* https://github.com/kovidgoyal/kitty/issues/6549

# Usage

## Simpliest

```sh
python layout_helper.py
```

## Full args

```sh
python layout_helper.py --config kitty.conf.example --map map.example --skip-macos --uncomment --no-backup
```

# Credits

Thanks to [Jakeroid](https://github.com/Jakeroid) for providing a great core concept
