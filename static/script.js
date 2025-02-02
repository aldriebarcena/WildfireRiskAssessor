document
  .getElementById("dataForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    const firstState = document.getElementById("firstState");
    const loadingAnimation = document.getElementById("loadingAnimation");
    firstState.style.display = "none";
    loadingAnimation.style.display = "block";

    async function isValidCity(city) {
      const apiKey = "AIzaSyDrq5VXjO6Aja69LTspzqWigseeg6NXL8I";
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`
      );
      const data = await response.json();
      return data.results && data.results.length > 0;
    }

    const city = data.city;
    try {
      const cityIsValid = await isValidCity(city);
      if (!cityIsValid) {
        loadingAnimation.style.display = "none";
        alert("Invalid city name. Please enter a valid city.");
        firstState.style.display = "block";
        return;
      }

      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });
      const result = await response.json();

      loadingAnimation.style.display = "none";
      document.getElementById("dataForm").style.display = "none";
      document.getElementById("secondState").style.display = "block";
      document.getElementById("header").textContent = "YOUR WILDFIRE RISK";

      const percentage = document.getElementById("percentage");
      percentage.textContent = `${result.percentage}%`;

      const ulElement = document.querySelector("ul");
      ulElement.innerHTML = ""; // Clear previous checklist
      result.checklist.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        ulElement.appendChild(li);
      });

      const body = document.body;
      if (result.percentage >= 80) {
        body.style.backgroundColor = "#c24036";
      } else if (result.percentage >= 60) {
        body.style.backgroundColor = "#bd7926";
      } else if (result.percentage >= 40) {
        body.style.backgroundColor = "#e6b925";
      } else if (result.percentage >= 20) {
        body.style.backgroundColor = "#fad24d";
      } else {
        body.style.backgroundColor = "gray";
      }
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("responseOutput").textContent =
        "An error occurred.";
    }

    loadingAnimation.style.display = "none";
  });
