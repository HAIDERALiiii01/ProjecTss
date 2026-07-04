# Media folder

The UI works with zero files in here — every card and detail page falls back
to generated placeholder art (a tinted gradient + the year) so nothing looks
broken. Drop in real files using this exact naming and they'll be picked up
automatically, no code changes needed.

For each entry, using its `id` from `data/winners.json` / `data/moments.json`:

```
assets/
  winners/
    2022/
      poster.jpg        <- static card image + detail hero fallback (~800x600)
      gif.gif            <- plays on card hover (~600x400, a few seconds, looping)
      gallery/
        1.jpg
        2.jpg
        3.jpg             <- up to 5, shown as a filmstrip on the detail page
  moments/
    messi-2022/
      poster.jpg
      gif.gif
      gallery/
        1.jpg
```

Notes:

- All files are optional and independent — you can add just a `poster.jpg`
  for one entry and nothing else, or just a `gif.gif` with no poster.
- I didn't source any images/gifs/video myself here since World Cup footage
  and photography are copyrighted — you'll want to pull your own from a
  licensed source (FIFA's media library, a stock provider, or your own
  clips) and drop them in following the structure above.
- Video isn't wired up in the JS yet (only image + gif). If you want actual
  video clips on the detail page hero, say the word and I'll add a
  `video.mp4` slot with a `<video>` element and play/pause controls.
