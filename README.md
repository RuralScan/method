# Rural Scan dashboard

[Open the dashboard](https://ruralscan.github.io/method/).

This branch publishes the existing static evidence dashboard on GitHub Pages. The interface and its data references are pinned to [CIAT release `bec50bc0f9dc`](https://github.com/CIAT/nbs_ruralscan/tree/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs). The deployment workflow packages the pinned dashboard and T4 JSON on the same origin as the interface. Source images link to that immutable revision. Live review runs in the CIAT checkout.

A push to `gh-pages` builds and deploys the Pages artifact. The methodology and cookbook are maintained on `main`.
