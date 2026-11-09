# First-impression estimates

`appearance` consumes a supplied raster or feature JSON. The caller chooses and records capture, viewport, crop and state. The frozen profile uses adjacent gradients, thresholded edge fractions, luminance entropy and colorfulness at independent 128/256/512 maximum-edge views. These are image properties, not gaze or feature congestion.

Four separate axes estimate average first impressions in the historical screenshot dataset: complexity, aesthetic appearance, craftsmanship and novelty. Complexity and novelty have no universally desirable direction. Craftsmanship means the impression named by that survey, not verified implementation quality. Outputs retain the original 1-7 training scale and remain unbounded; they are neither probabilities nor personal ratings. Feature distances are descriptive, not calibrated uncertainty.

The [human-rating dataset](https://doi.org/10.7910/DVN/XEYNYW) contains 1506 website screenshots from six collections. On 756 images from two collections held out from fitting, native-only rank correlations were .555 complexity, .445 appearance, .467 craftsmanship and .559 novelty. Absolute ratings were less consistently accurate than their rank order. The held-out images may still share brands or templates with those fitted.

An independent study rated full-page [banks](https://doi.org/10.7910/DVN/Z7KLIH), [shops](https://doi.org/10.7910/DVN/9FKSQI) and [universities](https://doi.org/10.7910/DVN/XOI0HI). Without refitting, native appearance estimates correlated .290 with full-page appearance ratings and .370 on a crop of the top 900 pixels. Those ratings measure perceived ease/trust from appearance, not actual usability or trust. Whole-page downsizing can erase text; full-page and viewport inputs are different conditions.

Blur, deleted details or empty layouts can improve a number while harming meaning. An appearance estimate can misrank real human-rated screens, and accurate complexity prediction does not imply appeal. Prefer no estimate when purpose, content, style, motion or audience differs enough to make the comparison contrived.

The profile estimates neither technical condition nor search duration; neither was reliable enough in evaluation to include. Geometry, visibility and the other instruments report supplied facts. Their arithmetic checks do not establish general UX validity.

No experiment here establishes causal improvement from using the design skill or hill climbing its estimates.
