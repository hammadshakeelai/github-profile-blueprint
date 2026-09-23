# 4 · What GitHub renders that almost nobody uses

Everything on this page is **native** — plain text in a markdown file that GitHub
itself turns into a map, a 3D model, a diagram or typeset maths. No image, no
service, nothing to go down. Code search found each of these on only a handful of
profiles ([chapter 2](02-curiosities.md#things-github-renders-that-almost-nobody-uses)).

Each exhibit below was checked on github.com after publishing; the results are
at the [bottom of the page](#verified).

---

## An interactive 3D model

GitHub renders an ASCII STL inside a ```` ```stl ```` fence as a model you can
spin and zoom. This one is built from real data: the last 24 months of repository
activity on [@hammadshakeelai](https://github.com/hammadshakeelai), one tower per
month, on a plinth — the same numbers as the showcase heatmap, as a city.

```stl
solid skyline
  facet normal 0 0 -1
    outer loop
      vertex -1.00 -1.00 0.00
      vertex 73.00 4.00 0.00
      vertex 73.00 -1.00 0.00
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex -1.00 -1.00 0.00
      vertex -1.00 4.00 0.00
      vertex 73.00 4.00 0.00
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex -1.00 -1.00 0.60
      vertex 73.00 -1.00 0.60
      vertex 73.00 4.00 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex -1.00 -1.00 0.60
      vertex 73.00 4.00 0.60
      vertex -1.00 4.00 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -1.00 -1.00 0.00
      vertex 73.00 -1.00 0.00
      vertex 73.00 -1.00 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex -1.00 -1.00 0.00
      vertex 73.00 -1.00 0.60
      vertex -1.00 -1.00 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 73.00 4.00 0.00
      vertex -1.00 4.00 0.00
      vertex -1.00 4.00 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 73.00 4.00 0.00
      vertex -1.00 4.00 0.60
      vertex 73.00 4.00 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 73.00 -1.00 0.00
      vertex 73.00 4.00 0.00
      vertex 73.00 4.00 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 73.00 -1.00 0.00
      vertex 73.00 4.00 0.60
      vertex 73.00 -1.00 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -1.00 -1.00 0.00
      vertex -1.00 -1.00 0.60
      vertex -1.00 4.00 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex -1.00 -1.00 0.00
      vertex -1.00 4.00 0.60
      vertex -1.00 4.00 0.00
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0.00 0.50 0.60
      vertex 2.00 2.50 0.60
      vertex 2.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 0.00 0.50 0.60
      vertex 0.00 2.50 0.60
      vertex 2.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0.00 0.50 0.60
      vertex 2.00 0.50 0.60
      vertex 2.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 0.00 0.50 0.60
      vertex 2.00 2.50 0.60
      vertex 0.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0.00 0.50 0.60
      vertex 2.00 0.50 0.60
      vertex 2.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 0.00 0.50 0.60
      vertex 2.00 0.50 0.60
      vertex 0.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 2.00 2.50 0.60
      vertex 0.00 2.50 0.60
      vertex 0.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 2.00 2.50 0.60
      vertex 0.00 2.50 0.60
      vertex 2.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2.00 0.50 0.60
      vertex 2.00 2.50 0.60
      vertex 2.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 2.00 0.50 0.60
      vertex 2.00 2.50 0.60
      vertex 2.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0.00 0.50 0.60
      vertex 0.00 0.50 0.60
      vertex 0.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 0.00 0.50 0.60
      vertex 0.00 2.50 0.60
      vertex 0.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 3.00 0.50 0.60
      vertex 5.00 2.50 0.60
      vertex 5.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 3.00 0.50 0.60
      vertex 3.00 2.50 0.60
      vertex 5.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 3.00 0.50 0.60
      vertex 5.00 0.50 0.60
      vertex 5.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 3.00 0.50 0.60
      vertex 5.00 2.50 0.60
      vertex 3.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 3.00 0.50 0.60
      vertex 5.00 0.50 0.60
      vertex 5.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 3.00 0.50 0.60
      vertex 5.00 0.50 0.60
      vertex 3.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 5.00 2.50 0.60
      vertex 3.00 2.50 0.60
      vertex 3.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 5.00 2.50 0.60
      vertex 3.00 2.50 0.60
      vertex 5.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 5.00 0.50 0.60
      vertex 5.00 2.50 0.60
      vertex 5.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 5.00 0.50 0.60
      vertex 5.00 2.50 0.60
      vertex 5.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 3.00 0.50 0.60
      vertex 3.00 0.50 0.60
      vertex 3.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 3.00 0.50 0.60
      vertex 3.00 2.50 0.60
      vertex 3.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 6.00 0.50 0.60
      vertex 8.00 2.50 0.60
      vertex 8.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 6.00 0.50 0.60
      vertex 6.00 2.50 0.60
      vertex 8.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 6.00 0.50 0.60
      vertex 8.00 0.50 0.60
      vertex 8.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 6.00 0.50 0.60
      vertex 8.00 2.50 0.60
      vertex 6.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 6.00 0.50 0.60
      vertex 8.00 0.50 0.60
      vertex 8.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 6.00 0.50 0.60
      vertex 8.00 0.50 0.60
      vertex 6.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 8.00 2.50 0.60
      vertex 6.00 2.50 0.60
      vertex 6.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 8.00 2.50 0.60
      vertex 6.00 2.50 0.60
      vertex 8.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 8.00 0.50 0.60
      vertex 8.00 2.50 0.60
      vertex 8.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 8.00 0.50 0.60
      vertex 8.00 2.50 0.60
      vertex 8.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 6.00 0.50 0.60
      vertex 6.00 0.50 0.60
      vertex 6.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 6.00 0.50 0.60
      vertex 6.00 2.50 0.60
      vertex 6.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 9.00 0.50 0.60
      vertex 11.00 2.50 0.60
      vertex 11.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 9.00 0.50 0.60
      vertex 9.00 2.50 0.60
      vertex 11.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 9.00 0.50 0.60
      vertex 11.00 0.50 0.60
      vertex 11.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 9.00 0.50 0.60
      vertex 11.00 2.50 0.60
      vertex 9.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 9.00 0.50 0.60
      vertex 11.00 0.50 0.60
      vertex 11.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 9.00 0.50 0.60
      vertex 11.00 0.50 0.60
      vertex 9.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 11.00 2.50 0.60
      vertex 9.00 2.50 0.60
      vertex 9.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 11.00 2.50 0.60
      vertex 9.00 2.50 0.60
      vertex 11.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 11.00 0.50 0.60
      vertex 11.00 2.50 0.60
      vertex 11.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 11.00 0.50 0.60
      vertex 11.00 2.50 0.60
      vertex 11.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 9.00 0.50 0.60
      vertex 9.00 0.50 0.60
      vertex 9.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 9.00 0.50 0.60
      vertex 9.00 2.50 0.60
      vertex 9.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 12.00 0.50 0.60
      vertex 14.00 2.50 0.60
      vertex 14.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 12.00 0.50 0.60
      vertex 12.00 2.50 0.60
      vertex 14.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 12.00 0.50 0.60
      vertex 14.00 0.50 0.60
      vertex 14.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 12.00 0.50 0.60
      vertex 14.00 2.50 0.60
      vertex 12.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 12.00 0.50 0.60
      vertex 14.00 0.50 0.60
      vertex 14.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 12.00 0.50 0.60
      vertex 14.00 0.50 0.60
      vertex 12.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 14.00 2.50 0.60
      vertex 12.00 2.50 0.60
      vertex 12.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 14.00 2.50 0.60
      vertex 12.00 2.50 0.60
      vertex 14.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 14.00 0.50 0.60
      vertex 14.00 2.50 0.60
      vertex 14.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 14.00 0.50 0.60
      vertex 14.00 2.50 0.60
      vertex 14.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 12.00 0.50 0.60
      vertex 12.00 0.50 0.60
      vertex 12.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 12.00 0.50 0.60
      vertex 12.00 2.50 0.60
      vertex 12.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 15.00 0.50 0.60
      vertex 17.00 2.50 0.60
      vertex 17.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 15.00 0.50 0.60
      vertex 15.00 2.50 0.60
      vertex 17.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 15.00 0.50 0.60
      vertex 17.00 0.50 0.60
      vertex 17.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 15.00 0.50 0.60
      vertex 17.00 2.50 0.60
      vertex 15.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 15.00 0.50 0.60
      vertex 17.00 0.50 0.60
      vertex 17.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 15.00 0.50 0.60
      vertex 17.00 0.50 0.60
      vertex 15.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 17.00 2.50 0.60
      vertex 15.00 2.50 0.60
      vertex 15.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 17.00 2.50 0.60
      vertex 15.00 2.50 0.60
      vertex 17.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 17.00 0.50 0.60
      vertex 17.00 2.50 0.60
      vertex 17.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 17.00 0.50 0.60
      vertex 17.00 2.50 0.60
      vertex 17.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 15.00 0.50 0.60
      vertex 15.00 0.50 0.60
      vertex 15.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 15.00 0.50 0.60
      vertex 15.00 2.50 0.60
      vertex 15.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 18.00 0.50 0.60
      vertex 20.00 2.50 0.60
      vertex 20.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 18.00 0.50 0.60
      vertex 18.00 2.50 0.60
      vertex 20.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 18.00 0.50 0.60
      vertex 20.00 0.50 0.60
      vertex 20.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 18.00 0.50 0.60
      vertex 20.00 2.50 0.60
      vertex 18.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 18.00 0.50 0.60
      vertex 20.00 0.50 0.60
      vertex 20.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 18.00 0.50 0.60
      vertex 20.00 0.50 0.60
      vertex 18.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 20.00 2.50 0.60
      vertex 18.00 2.50 0.60
      vertex 18.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 20.00 2.50 0.60
      vertex 18.00 2.50 0.60
      vertex 20.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 20.00 0.50 0.60
      vertex 20.00 2.50 0.60
      vertex 20.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 20.00 0.50 0.60
      vertex 20.00 2.50 0.60
      vertex 20.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 18.00 0.50 0.60
      vertex 18.00 0.50 0.60
      vertex 18.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 18.00 0.50 0.60
      vertex 18.00 2.50 0.60
      vertex 18.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 21.00 0.50 0.60
      vertex 23.00 2.50 0.60
      vertex 23.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 21.00 0.50 0.60
      vertex 21.00 2.50 0.60
      vertex 23.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 21.00 0.50 2.47
      vertex 23.00 0.50 2.47
      vertex 23.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 21.00 0.50 2.47
      vertex 23.00 2.50 2.47
      vertex 21.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 21.00 0.50 0.60
      vertex 23.00 0.50 0.60
      vertex 23.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 21.00 0.50 0.60
      vertex 23.00 0.50 2.47
      vertex 21.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 23.00 2.50 0.60
      vertex 21.00 2.50 0.60
      vertex 21.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 23.00 2.50 0.60
      vertex 21.00 2.50 2.47
      vertex 23.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 23.00 0.50 0.60
      vertex 23.00 2.50 0.60
      vertex 23.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 23.00 0.50 0.60
      vertex 23.00 2.50 2.47
      vertex 23.00 0.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 21.00 0.50 0.60
      vertex 21.00 0.50 2.47
      vertex 21.00 2.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 21.00 0.50 0.60
      vertex 21.00 2.50 2.47
      vertex 21.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 24.00 0.50 0.60
      vertex 26.00 2.50 0.60
      vertex 26.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 24.00 0.50 0.60
      vertex 24.00 2.50 0.60
      vertex 26.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 24.00 0.50 0.60
      vertex 26.00 0.50 0.60
      vertex 26.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 24.00 0.50 0.60
      vertex 26.00 2.50 0.60
      vertex 24.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 24.00 0.50 0.60
      vertex 26.00 0.50 0.60
      vertex 26.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 24.00 0.50 0.60
      vertex 26.00 0.50 0.60
      vertex 24.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 26.00 2.50 0.60
      vertex 24.00 2.50 0.60
      vertex 24.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 26.00 2.50 0.60
      vertex 24.00 2.50 0.60
      vertex 26.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 26.00 0.50 0.60
      vertex 26.00 2.50 0.60
      vertex 26.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 26.00 0.50 0.60
      vertex 26.00 2.50 0.60
      vertex 26.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 24.00 0.50 0.60
      vertex 24.00 0.50 0.60
      vertex 24.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 24.00 0.50 0.60
      vertex 24.00 2.50 0.60
      vertex 24.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 27.00 0.50 0.60
      vertex 29.00 2.50 0.60
      vertex 29.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 27.00 0.50 0.60
      vertex 27.00 2.50 0.60
      vertex 29.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 27.00 0.50 1.07
      vertex 29.00 0.50 1.07
      vertex 29.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 27.00 0.50 1.07
      vertex 29.00 2.50 1.07
      vertex 27.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 27.00 0.50 0.60
      vertex 29.00 0.50 0.60
      vertex 29.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 27.00 0.50 0.60
      vertex 29.00 0.50 1.07
      vertex 27.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 29.00 2.50 0.60
      vertex 27.00 2.50 0.60
      vertex 27.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 29.00 2.50 0.60
      vertex 27.00 2.50 1.07
      vertex 29.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 29.00 0.50 0.60
      vertex 29.00 2.50 0.60
      vertex 29.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 29.00 0.50 0.60
      vertex 29.00 2.50 1.07
      vertex 29.00 0.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 27.00 0.50 0.60
      vertex 27.00 0.50 1.07
      vertex 27.00 2.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 27.00 0.50 0.60
      vertex 27.00 2.50 1.07
      vertex 27.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 30.00 0.50 0.60
      vertex 32.00 2.50 0.60
      vertex 32.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 30.00 0.50 0.60
      vertex 30.00 2.50 0.60
      vertex 32.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 30.00 0.50 2.93
      vertex 32.00 0.50 2.93
      vertex 32.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 30.00 0.50 2.93
      vertex 32.00 2.50 2.93
      vertex 30.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 30.00 0.50 0.60
      vertex 32.00 0.50 0.60
      vertex 32.00 0.50 2.93
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 30.00 0.50 0.60
      vertex 32.00 0.50 2.93
      vertex 30.00 0.50 2.93
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 32.00 2.50 0.60
      vertex 30.00 2.50 0.60
      vertex 30.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 32.00 2.50 0.60
      vertex 30.00 2.50 2.93
      vertex 32.00 2.50 2.93
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 32.00 0.50 0.60
      vertex 32.00 2.50 0.60
      vertex 32.00 2.50 2.93
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 32.00 0.50 0.60
      vertex 32.00 2.50 2.93
      vertex 32.00 0.50 2.93
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 30.00 0.50 0.60
      vertex 30.00 0.50 2.93
      vertex 30.00 2.50 2.93
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 30.00 0.50 0.60
      vertex 30.00 2.50 2.93
      vertex 30.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 33.00 0.50 0.60
      vertex 35.00 2.50 0.60
      vertex 35.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 33.00 0.50 0.60
      vertex 33.00 2.50 0.60
      vertex 35.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 33.00 0.50 0.60
      vertex 35.00 0.50 0.60
      vertex 35.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 33.00 0.50 0.60
      vertex 35.00 2.50 0.60
      vertex 33.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 33.00 0.50 0.60
      vertex 35.00 0.50 0.60
      vertex 35.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 33.00 0.50 0.60
      vertex 35.00 0.50 0.60
      vertex 33.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 35.00 2.50 0.60
      vertex 33.00 2.50 0.60
      vertex 33.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 35.00 2.50 0.60
      vertex 33.00 2.50 0.60
      vertex 35.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 35.00 0.50 0.60
      vertex 35.00 2.50 0.60
      vertex 35.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 35.00 0.50 0.60
      vertex 35.00 2.50 0.60
      vertex 35.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 33.00 0.50 0.60
      vertex 33.00 0.50 0.60
      vertex 33.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 33.00 0.50 0.60
      vertex 33.00 2.50 0.60
      vertex 33.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 36.00 0.50 0.60
      vertex 38.00 2.50 0.60
      vertex 38.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 36.00 0.50 0.60
      vertex 36.00 2.50 0.60
      vertex 38.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 36.00 0.50 1.07
      vertex 38.00 0.50 1.07
      vertex 38.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 36.00 0.50 1.07
      vertex 38.00 2.50 1.07
      vertex 36.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 36.00 0.50 0.60
      vertex 38.00 0.50 0.60
      vertex 38.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 36.00 0.50 0.60
      vertex 38.00 0.50 1.07
      vertex 36.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 38.00 2.50 0.60
      vertex 36.00 2.50 0.60
      vertex 36.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 38.00 2.50 0.60
      vertex 36.00 2.50 1.07
      vertex 38.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 38.00 0.50 0.60
      vertex 38.00 2.50 0.60
      vertex 38.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 38.00 0.50 0.60
      vertex 38.00 2.50 1.07
      vertex 38.00 0.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 36.00 0.50 0.60
      vertex 36.00 0.50 1.07
      vertex 36.00 2.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 36.00 0.50 0.60
      vertex 36.00 2.50 1.07
      vertex 36.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 39.00 0.50 0.60
      vertex 41.00 2.50 0.60
      vertex 41.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 39.00 0.50 0.60
      vertex 39.00 2.50 0.60
      vertex 41.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 39.00 0.50 0.60
      vertex 41.00 0.50 0.60
      vertex 41.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 39.00 0.50 0.60
      vertex 41.00 2.50 0.60
      vertex 39.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 39.00 0.50 0.60
      vertex 41.00 0.50 0.60
      vertex 41.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 39.00 0.50 0.60
      vertex 41.00 0.50 0.60
      vertex 39.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 41.00 2.50 0.60
      vertex 39.00 2.50 0.60
      vertex 39.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 41.00 2.50 0.60
      vertex 39.00 2.50 0.60
      vertex 41.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 41.00 0.50 0.60
      vertex 41.00 2.50 0.60
      vertex 41.00 2.50 0.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 41.00 0.50 0.60
      vertex 41.00 2.50 0.60
      vertex 41.00 0.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 39.00 0.50 0.60
      vertex 39.00 0.50 0.60
      vertex 39.00 2.50 0.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 39.00 0.50 0.60
      vertex 39.00 2.50 0.60
      vertex 39.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 42.00 0.50 0.60
      vertex 44.00 2.50 0.60
      vertex 44.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 42.00 0.50 0.60
      vertex 42.00 2.50 0.60
      vertex 44.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 42.00 0.50 1.07
      vertex 44.00 0.50 1.07
      vertex 44.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 42.00 0.50 1.07
      vertex 44.00 2.50 1.07
      vertex 42.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 42.00 0.50 0.60
      vertex 44.00 0.50 0.60
      vertex 44.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 42.00 0.50 0.60
      vertex 44.00 0.50 1.07
      vertex 42.00 0.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 44.00 2.50 0.60
      vertex 42.00 2.50 0.60
      vertex 42.00 2.50 1.07
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 44.00 2.50 0.60
      vertex 42.00 2.50 1.07
      vertex 44.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 44.00 0.50 0.60
      vertex 44.00 2.50 0.60
      vertex 44.00 2.50 1.07
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 44.00 0.50 0.60
      vertex 44.00 2.50 1.07
      vertex 44.00 0.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 42.00 0.50 0.60
      vertex 42.00 0.50 1.07
      vertex 42.00 2.50 1.07
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 42.00 0.50 0.60
      vertex 42.00 2.50 1.07
      vertex 42.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 45.00 0.50 0.60
      vertex 47.00 2.50 0.60
      vertex 47.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 45.00 0.50 0.60
      vertex 45.00 2.50 0.60
      vertex 47.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 45.00 0.50 2.47
      vertex 47.00 0.50 2.47
      vertex 47.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 45.00 0.50 2.47
      vertex 47.00 2.50 2.47
      vertex 45.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 45.00 0.50 0.60
      vertex 47.00 0.50 0.60
      vertex 47.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 45.00 0.50 0.60
      vertex 47.00 0.50 2.47
      vertex 45.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 47.00 2.50 0.60
      vertex 45.00 2.50 0.60
      vertex 45.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 47.00 2.50 0.60
      vertex 45.00 2.50 2.47
      vertex 47.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 47.00 0.50 0.60
      vertex 47.00 2.50 0.60
      vertex 47.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 47.00 0.50 0.60
      vertex 47.00 2.50 2.47
      vertex 47.00 0.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 45.00 0.50 0.60
      vertex 45.00 0.50 2.47
      vertex 45.00 2.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 45.00 0.50 0.60
      vertex 45.00 2.50 2.47
      vertex 45.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 48.00 0.50 0.60
      vertex 50.00 2.50 0.60
      vertex 50.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 48.00 0.50 0.60
      vertex 48.00 2.50 0.60
      vertex 50.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 48.00 0.50 2.00
      vertex 50.00 0.50 2.00
      vertex 50.00 2.50 2.00
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 48.00 0.50 2.00
      vertex 50.00 2.50 2.00
      vertex 48.00 2.50 2.00
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 48.00 0.50 0.60
      vertex 50.00 0.50 0.60
      vertex 50.00 0.50 2.00
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 48.00 0.50 0.60
      vertex 50.00 0.50 2.00
      vertex 48.00 0.50 2.00
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 50.00 2.50 0.60
      vertex 48.00 2.50 0.60
      vertex 48.00 2.50 2.00
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 50.00 2.50 0.60
      vertex 48.00 2.50 2.00
      vertex 50.00 2.50 2.00
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 50.00 0.50 0.60
      vertex 50.00 2.50 0.60
      vertex 50.00 2.50 2.00
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 50.00 0.50 0.60
      vertex 50.00 2.50 2.00
      vertex 50.00 0.50 2.00
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 48.00 0.50 0.60
      vertex 48.00 0.50 2.00
      vertex 48.00 2.50 2.00
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 48.00 0.50 0.60
      vertex 48.00 2.50 2.00
      vertex 48.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 51.00 0.50 0.60
      vertex 53.00 2.50 0.60
      vertex 53.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 51.00 0.50 0.60
      vertex 51.00 2.50 0.60
      vertex 53.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 51.00 0.50 1.53
      vertex 53.00 0.50 1.53
      vertex 53.00 2.50 1.53
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 51.00 0.50 1.53
      vertex 53.00 2.50 1.53
      vertex 51.00 2.50 1.53
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 51.00 0.50 0.60
      vertex 53.00 0.50 0.60
      vertex 53.00 0.50 1.53
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 51.00 0.50 0.60
      vertex 53.00 0.50 1.53
      vertex 51.00 0.50 1.53
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 53.00 2.50 0.60
      vertex 51.00 2.50 0.60
      vertex 51.00 2.50 1.53
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 53.00 2.50 0.60
      vertex 51.00 2.50 1.53
      vertex 53.00 2.50 1.53
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 53.00 0.50 0.60
      vertex 53.00 2.50 0.60
      vertex 53.00 2.50 1.53
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 53.00 0.50 0.60
      vertex 53.00 2.50 1.53
      vertex 53.00 0.50 1.53
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 51.00 0.50 0.60
      vertex 51.00 0.50 1.53
      vertex 51.00 2.50 1.53
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 51.00 0.50 0.60
      vertex 51.00 2.50 1.53
      vertex 51.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 54.00 0.50 0.60
      vertex 56.00 2.50 0.60
      vertex 56.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 54.00 0.50 0.60
      vertex 54.00 2.50 0.60
      vertex 56.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 54.00 0.50 5.27
      vertex 56.00 0.50 5.27
      vertex 56.00 2.50 5.27
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 54.00 0.50 5.27
      vertex 56.00 2.50 5.27
      vertex 54.00 2.50 5.27
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 54.00 0.50 0.60
      vertex 56.00 0.50 0.60
      vertex 56.00 0.50 5.27
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 54.00 0.50 0.60
      vertex 56.00 0.50 5.27
      vertex 54.00 0.50 5.27
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 56.00 2.50 0.60
      vertex 54.00 2.50 0.60
      vertex 54.00 2.50 5.27
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 56.00 2.50 0.60
      vertex 54.00 2.50 5.27
      vertex 56.00 2.50 5.27
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 56.00 0.50 0.60
      vertex 56.00 2.50 0.60
      vertex 56.00 2.50 5.27
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 56.00 0.50 0.60
      vertex 56.00 2.50 5.27
      vertex 56.00 0.50 5.27
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 54.00 0.50 0.60
      vertex 54.00 0.50 5.27
      vertex 54.00 2.50 5.27
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 54.00 0.50 0.60
      vertex 54.00 2.50 5.27
      vertex 54.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 57.00 0.50 0.60
      vertex 59.00 2.50 0.60
      vertex 59.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 57.00 0.50 0.60
      vertex 57.00 2.50 0.60
      vertex 59.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 57.00 0.50 4.80
      vertex 59.00 0.50 4.80
      vertex 59.00 2.50 4.80
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 57.00 0.50 4.80
      vertex 59.00 2.50 4.80
      vertex 57.00 2.50 4.80
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 57.00 0.50 0.60
      vertex 59.00 0.50 0.60
      vertex 59.00 0.50 4.80
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 57.00 0.50 0.60
      vertex 59.00 0.50 4.80
      vertex 57.00 0.50 4.80
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 59.00 2.50 0.60
      vertex 57.00 2.50 0.60
      vertex 57.00 2.50 4.80
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 59.00 2.50 0.60
      vertex 57.00 2.50 4.80
      vertex 59.00 2.50 4.80
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 59.00 0.50 0.60
      vertex 59.00 2.50 0.60
      vertex 59.00 2.50 4.80
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 59.00 0.50 0.60
      vertex 59.00 2.50 4.80
      vertex 59.00 0.50 4.80
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 57.00 0.50 0.60
      vertex 57.00 0.50 4.80
      vertex 57.00 2.50 4.80
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 57.00 0.50 0.60
      vertex 57.00 2.50 4.80
      vertex 57.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 60.00 0.50 0.60
      vertex 62.00 2.50 0.60
      vertex 62.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 60.00 0.50 0.60
      vertex 60.00 2.50 0.60
      vertex 62.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 60.00 0.50 2.93
      vertex 62.00 0.50 2.93
      vertex 62.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 60.00 0.50 2.93
      vertex 62.00 2.50 2.93
      vertex 60.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 60.00 0.50 0.60
      vertex 62.00 0.50 0.60
      vertex 62.00 0.50 2.93
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 60.00 0.50 0.60
      vertex 62.00 0.50 2.93
      vertex 60.00 0.50 2.93
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 62.00 2.50 0.60
      vertex 60.00 2.50 0.60
      vertex 60.00 2.50 2.93
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 62.00 2.50 0.60
      vertex 60.00 2.50 2.93
      vertex 62.00 2.50 2.93
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 62.00 0.50 0.60
      vertex 62.00 2.50 0.60
      vertex 62.00 2.50 2.93
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 62.00 0.50 0.60
      vertex 62.00 2.50 2.93
      vertex 62.00 0.50 2.93
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 60.00 0.50 0.60
      vertex 60.00 0.50 2.93
      vertex 60.00 2.50 2.93
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 60.00 0.50 0.60
      vertex 60.00 2.50 2.93
      vertex 60.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 63.00 0.50 0.60
      vertex 65.00 2.50 0.60
      vertex 65.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 63.00 0.50 0.60
      vertex 63.00 2.50 0.60
      vertex 65.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 63.00 0.50 3.87
      vertex 65.00 0.50 3.87
      vertex 65.00 2.50 3.87
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 63.00 0.50 3.87
      vertex 65.00 2.50 3.87
      vertex 63.00 2.50 3.87
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 63.00 0.50 0.60
      vertex 65.00 0.50 0.60
      vertex 65.00 0.50 3.87
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 63.00 0.50 0.60
      vertex 65.00 0.50 3.87
      vertex 63.00 0.50 3.87
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 65.00 2.50 0.60
      vertex 63.00 2.50 0.60
      vertex 63.00 2.50 3.87
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 65.00 2.50 0.60
      vertex 63.00 2.50 3.87
      vertex 65.00 2.50 3.87
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 65.00 0.50 0.60
      vertex 65.00 2.50 0.60
      vertex 65.00 2.50 3.87
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 65.00 0.50 0.60
      vertex 65.00 2.50 3.87
      vertex 65.00 0.50 3.87
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 63.00 0.50 0.60
      vertex 63.00 0.50 3.87
      vertex 63.00 2.50 3.87
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 63.00 0.50 0.60
      vertex 63.00 2.50 3.87
      vertex 63.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 66.00 0.50 0.60
      vertex 68.00 2.50 0.60
      vertex 68.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 66.00 0.50 0.60
      vertex 66.00 2.50 0.60
      vertex 68.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 66.00 0.50 2.47
      vertex 68.00 0.50 2.47
      vertex 68.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 66.00 0.50 2.47
      vertex 68.00 2.50 2.47
      vertex 66.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 66.00 0.50 0.60
      vertex 68.00 0.50 0.60
      vertex 68.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 66.00 0.50 0.60
      vertex 68.00 0.50 2.47
      vertex 66.00 0.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 68.00 2.50 0.60
      vertex 66.00 2.50 0.60
      vertex 66.00 2.50 2.47
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 68.00 2.50 0.60
      vertex 66.00 2.50 2.47
      vertex 68.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 68.00 0.50 0.60
      vertex 68.00 2.50 0.60
      vertex 68.00 2.50 2.47
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 68.00 0.50 0.60
      vertex 68.00 2.50 2.47
      vertex 68.00 0.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 66.00 0.50 0.60
      vertex 66.00 0.50 2.47
      vertex 66.00 2.50 2.47
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 66.00 0.50 0.60
      vertex 66.00 2.50 2.47
      vertex 66.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 69.00 0.50 0.60
      vertex 71.00 2.50 0.60
      vertex 71.00 0.50 0.60
    endloop
  endfacet
  facet normal 0 0 -1
    outer loop
      vertex 69.00 0.50 0.60
      vertex 69.00 2.50 0.60
      vertex 71.00 2.50 0.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 69.00 0.50 14.60
      vertex 71.00 0.50 14.60
      vertex 71.00 2.50 14.60
    endloop
  endfacet
  facet normal 0 0 1
    outer loop
      vertex 69.00 0.50 14.60
      vertex 71.00 2.50 14.60
      vertex 69.00 2.50 14.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 69.00 0.50 0.60
      vertex 71.00 0.50 0.60
      vertex 71.00 0.50 14.60
    endloop
  endfacet
  facet normal 0 -1 0
    outer loop
      vertex 69.00 0.50 0.60
      vertex 71.00 0.50 14.60
      vertex 69.00 0.50 14.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 71.00 2.50 0.60
      vertex 69.00 2.50 0.60
      vertex 69.00 2.50 14.60
    endloop
  endfacet
  facet normal 0 1 0
    outer loop
      vertex 71.00 2.50 0.60
      vertex 69.00 2.50 14.60
      vertex 71.00 2.50 14.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 71.00 0.50 0.60
      vertex 71.00 2.50 0.60
      vertex 71.00 2.50 14.60
    endloop
  endfacet
  facet normal 1 0 0
    outer loop
      vertex 71.00 0.50 0.60
      vertex 71.00 2.50 14.60
      vertex 71.00 0.50 14.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 69.00 0.50 0.60
      vertex 69.00 0.50 14.60
      vertex 69.00 2.50 14.60
    endloop
  endfacet
  facet normal -1 0 0
    outer loop
      vertex 69.00 0.50 0.60
      vertex 69.00 2.50 14.60
      vertex 69.00 2.50 0.60
    endloop
  endfacet
endsolid skyline
```

Generated by [`tools/book/native.py`](../../tools/book/native.py) — 300
triangles, 42 KB. GitHub stops rendering past 512 KB of markdown;
[readme-3d](https://github.com/nirholas/readme-3d) simplifies bigger meshes to fit.
The same file is 3D-printable.

---

## An interactive map

A ```` ```geojson ```` fence becomes a pannable map. Plotted: the most-copied
profile READMEs on GitHub, at the location each author gives on their profile
(pink = over 1,000 stars). Profiles that state no location are left off rather
than guessed.

```geojson
{
 "type": "FeatureCollection",
 "features": [
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     -50.22,
     -27.24
    ]
   },
   "properties": {
    "profile": "github.com/rafaballerini",
    "stars": 2696,
    "location": "Santa Catarina, Brazil",
    "marker-size": "large",
    "marker-color": "#f778ba"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     2.17,
     41.39
    ]
   },
   "properties": {
    "profile": "github.com/midudev",
    "stars": 1465,
    "location": "Barcelona",
    "marker-size": "large",
    "marker-color": "#f778ba"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     -79.38,
     43.65
    ]
   },
   "properties": {
    "profile": "github.com/novatorem",
    "stars": 758,
    "location": "Toronto",
    "marker-size": "medium",
    "marker-color": "#58a6ff"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     55.27,
     25.2
    ]
   },
   "properties": {
    "profile": "github.com/anmol098",
    "stars": 689,
    "location": "Dubai",
    "marker-size": "medium",
    "marker-color": "#58a6ff"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     -61.22,
     10.69
    ]
   },
   "properties": {
    "profile": "github.com/trinib",
    "stars": 508,
    "location": "Trinidad & Tobago",
    "marker-size": "medium",
    "marker-color": "#58a6ff"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     -122.43,
     37.46
    ]
   },
   "properties": {
    "profile": "github.com/simonw",
    "stars": 443,
    "location": "Half Moon Bay, California",
    "marker-size": "small",
    "marker-color": "#58a6ff"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     17.11,
     48.15
    ]
   },
   "properties": {
    "profile": "github.com/MartinHeinz",
    "stars": 440,
    "location": "Bratislava",
    "marker-size": "small",
    "marker-color": "#58a6ff"
   }
  },
  {
   "type": "Feature",
   "geometry": {
    "type": "Point",
    "coordinates": [
     -122.42,
     37.77
    ]
   },
   "properties": {
    "profile": "github.com/andyruwruw",
    "stars": 290,
    "location": "Bay Area, California",
    "marker-size": "small",
    "marker-color": "#58a6ff"
   }
  }
 ]
}
```

---

## Diagrams that stay sharp at any width

Mermaid is text, so it reflows and never pixelates — the one kind of "graphic"
that is automatically legible on a phone.

### A mind-map (what [pr2tik1](https://github.com/pr2tik1) uses as a skills section)

```mermaid
mindmap
  root((Profile README))
    Playable
      Royal Game of Ur
      Community chess
      Connect Four
      Word cloud
    Live
      Now playing
      Discord presence
      Server telemetry
      Chess games
    Grown
      Kodama bonsai
      Arcade contribution games
      Matrix rain
    Native
      STL models
      GeoJSON maps
      Mermaid
      LaTeX
```

### A timeline

```mermaid
timeline
    title Profile READMEs, the short history
    2020 : Profile READMEs launch
         : Simon Willison publishes the self-updating README (July)
    2022 : Mermaid, GeoJSON, TopoJSON and ASCII STL render in markdown (March)
    2024 : RevolverMaps visitor globes shut down
    2026 : ClustrMaps unreachable
         : The public github-readme-stats instance loads 0% of the time
```

### A chart of this book's own sources

```mermaid
pie showData
    title Items found by web search, by kind
    "live-data" : 12
    "contribution-art" : 10
    "cards" : 7
    "visitors" : 5
    "theme" : 4
    "game" : 4
    "badges" : 4
    "generative-art" : 3
    "portrait-art" : 3
    "terminal" : 3
    "banner" : 3
    "layout" : 3
    "generator" : 2
    "native-render" : 2
    "automation" : 2
    "media" : 2
    "easter-egg" : 1
    "reference" : 1
```

---

## Typeset maths

The rule that decides whether a banner can be read on a phone, stated exactly:

$$F_{\min} = 	ext{target} 	imes rac{W}{R}$$

---

## Alerts, all five

> [!NOTE]
> Useful information the reader should know.

> [!TIP]
> Helpful advice.

> [!IMPORTANT]
> Key information.

> [!WARNING]
> Urgent information that needs attention.

> [!CAUTION]
> Risks or negative outcomes.

---

## Small things

- A footnote reference.[^why]
- Keyboard keys: <kbd>Ctrl</kbd> + <kbd>K</kbd>
- A task list:
  - [x] rendered by GitHub
  - [ ] rendered everywhere else

<details>
<summary><b>A collapsed section</b> — click to open</summary>

Anything can live in here, including images and tables, and it costs no vertical
space until someone asks for it.

</details>

[^why]: Footnotes render as numbered links with a back-reference at the bottom.

---

## Which inline HTML survives?

The line below uses nine rarely-used tags. GitHub's sanitizer keeps some and
strips others; which is which was read back from the rendered page.

<p id="probe">
<ruby>漢<rp>(</rp><rt>kan</rt><rp>)</rp></ruby> ·
<ins>inserted</ins> ·
<del>deleted</del> ·
<sup>sup</sup> / <sub>sub</sub> ·
<samp>sample output</samp> ·
<var>variable</var> ·
<mark>marked</mark> ·
<abbr title="HyperText Markup Language">HTML</abbr> ·
<q>quoted</q>
</p>

---

## Verified

_Filled in after publishing — see below._
