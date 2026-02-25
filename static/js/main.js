(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  if (!toggle || !nav) return;

  const setOpen = (open) => {
    nav.classList.toggle("open", open);
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
  };

  toggle.addEventListener("click", () => {
    const isOpen = nav.classList.contains("open");
    setOpen(!isOpen);
  });

  // Close on outside click
  document.addEventListener("click", (e) => {
    if (!nav.classList.contains("open")) return;
    if (nav.contains(e.target) || toggle.contains(e.target)) return;
    setOpen(false);
  });

  // Close on ESC
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
})();

// Testimonial slider (no libraries)
(() => {
  const slider = document.getElementById("tSlider");
  if (!slider) return;

  const track = slider.querySelector(".t-track");
  const slides = Array.from(slider.querySelectorAll(".t-slide"));
  const dots = Array.from(slider.querySelectorAll(".t-dot"));
  const prevBtn = slider.querySelector(".t-prev");
  const nextBtn = slider.querySelector(".t-next");

  let index = 0;
  let timer = null;

  const setActiveDot = (i) => {
    dots.forEach((d, idx) => d.classList.toggle("active", idx === i));
  };

  const goTo = (i) => {
    index = (i + slides.length) % slides.length;
    track.style.transform = `translateX(-${index * 100}%)`;
    setActiveDot(index);
  };

  const start = () => {
    stop();
    timer = setInterval(() => goTo(index + 1), 4500);
  };

  const stop = () => {
    if (timer) clearInterval(timer);
    timer = null;
  };

  // Buttons
  prevBtn?.addEventListener("click", () => goTo(index - 1));
  nextBtn?.addEventListener("click", () => goTo(index + 1));

  // Dots
  dots.forEach((dot, i) => dot.addEventListener("click", () => goTo(i)));

  // Pause on hover/focus
  slider.addEventListener("mouseenter", stop);
  slider.addEventListener("mouseleave", start);
  slider.addEventListener("focusin", stop);
  slider.addEventListener("focusout", start);

  // Init
  goTo(0);
  start();
})();