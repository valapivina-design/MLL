(function () {
  var form = document.getElementById("insight-comment-form");
  if (!form) return;
  var status = document.getElementById("comment-form-status");
  var btn = document.getElementById("comment-submit");
  var urlEl = document.getElementById("comment-page-url");
  if (urlEl) urlEl.value = window.location.href;
  var lead = form.elements.lead_source ? form.elements.lead_source.value : "";
  var topic = form.elements.topic ? form.elements.topic.value : "";

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (status) {
      status.textContent = "";
      status.className = "comment-form-status";
    }
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }
    if (urlEl) urlEl.value = window.location.href;
    if (btn) btn.disabled = true;
    if (status) status.textContent = "Sending…";

    fetch(form.action, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(form),
    })
      .then(function (res) {
        return res.json().then(function (data) {
          return { ok: res.ok, data: data };
        });
      })
      .then(function (result) {
        var data = result.data || {};
        if (result.ok && (data.code === 200 || data.status === "success")) {
          if (status) {
            status.className = "comment-form-status ok";
            status.textContent =
              "Thank you. Your comment was received and will be moderated before it appears live.";
          }
          form.reset();
          if (form.elements.form_type) form.elements.form_type.value = "comment";
          if (form.elements.lead_source) form.elements.lead_source.value = lead;
          if (form.elements.topic) form.elements.topic.value = topic;
          if (urlEl) urlEl.value = window.location.href;
        } else {
          if (status) {
            status.className = "comment-form-status err";
            status.textContent =
              (data && data.message) ||
              "We could not submit that comment. Please try again in a moment.";
          }
        }
      })
      .catch(function () {
        if (status) {
          status.className = "comment-form-status err";
          status.textContent = "No response from the form service. Please try again.";
        }
      })
      .finally(function () {
        if (btn) btn.disabled = false;
      });
  });
})();
