document.querySelectorAll("form[data-confirm]").forEach((form) => {
  form.addEventListener("submit", (event) => {
    if (!window.confirm(form.dataset.confirm || "Are you sure?")) {
      event.preventDefault();
    }
  });
});

document.querySelectorAll(".flash").forEach((flash) => {
  window.setTimeout(() => {
    if (flash.isConnected) flash.classList.add("flash-hide");
  }, 5000);
});

const dateInput = document.querySelector("#start-date");
if (dateInput && !dateInput.value) {
  dateInput.value = new Date().toISOString().slice(0, 10);
}
