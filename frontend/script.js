// Handle form submission via JS for dynamic result display
const form = document.getElementById("queryForm");
const resultsDiv = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            resultsDiv.innerHTML = `<p style="color:red;">Error: ${response.statusText}</p>`;
            return;
        }

        const html = await response.text();
        resultsDiv.innerHTML = html;
    } catch (err) {
        resultsDiv.innerHTML = `<p style="color:red;">Exception: ${err}</p>`;
    }
});
