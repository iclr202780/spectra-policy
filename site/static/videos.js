// Start each excerpt once when it comes into view. Native controls remain available.
// Keep posters and manual playback for visitors who prefer reduced motion.
(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;
  const videos = document.querySelectorAll('video[data-play-in-view]');
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      observer.unobserve(entry.target);
      if (!reducedMotion.matches) entry.target.play().catch(() => {});
    }
  }, { threshold: 0.25 });
  videos.forEach(video => observer.observe(video));
  reducedMotion.addEventListener('change', event => {
    if (event.matches) videos.forEach(video => video.pause());
  });
})();
