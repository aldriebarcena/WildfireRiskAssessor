document
  .getElementById("dataForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault(); // Prevents the form's default behavior
    const form = event.target;
    const formData = new FormData(form);
    const data = {};
    formData.forEach((value, key) => {
      data[key] = value;
    });

    async function isValidCity(city) {
      const apiKey = "AIzaSyDrq5VXjO6Aja69LTspzqWigseeg6NXL8I";
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`
      );
      const data = await response.json();
      console.log(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`
      );
      return data.results && data.results.length > 0;
    }
    console.log(data);
    const city = data.city;

    try {
      const cityIsValid = await isValidCity(city);
      if (!cityIsValid) {
        alert("Invalid city name. Please enter a valid city.");
        return;
      }

      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();

      // Hide the first form (dataForm)
      document.getElementById("dataForm").style.display = "none";

      // Show the second form (changeBkg)
      document.getElementById("changeBkg").style.display = "block";

      // update percentage
      const percentage = document.getElementById("percentage");
      percentage.textContent = `${result.percentage}%`;

      // update checklist
      const ulElement = document.querySelector("ul");
      result.checklist.forEach((item) => {
        const li = document.createElement("li");
        li.textContent = item;
        ulElement.appendChild(li);
      });

      // change background color based on percentage
      const body = document.body;

      if (result.percentage >= 80) {
        body.style.backgroundColor = "green";
      } else if (result.percentage >= 60) {
        body.style.backgroundColor = "yellow";
      } else if (result.percentage >= 40) {
        body.style.backgroundColor = "orange";
      } else if (result.percentage >= 20) {
        body.style.backgroundColor = "red";
      } else {
        body.style.backgroundColor = "gray";
      }
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("responseOutput").textContent =
        "An error occurred.";
    }
  });
