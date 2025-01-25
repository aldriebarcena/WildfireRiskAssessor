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

    // Function to validate city name
    async function isValidCity(city) {
      const apiKey = "AIzaSyDrq5VXjO6Aja69LTspzqWigseeg6NXL8I"; // Replace with your actual API key
      const response = await fetch(
        `https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`
      );
      const data = await response.json();
      console.log(`https://maps.googleapis.com/maps/api/geocode/json?address=${city}&key=${apiKey}`)
      // If no results are returned, city is invalid
      return data.results && data.results.length > 0;
    }
    console.log(data)
    // Assuming the form data includes a 'city' field
    const city = data.city;

    try {
      // Validate the city
      const cityIsValid = await isValidCity(city);
      if (!cityIsValid) {
        alert("Invalid city name. Please enter a valid city.");
        return; // Stop form submission if the city is invalid
      }

      // If the city is valid, proceed with form submission
      const response = await fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      document.getElementById(
        "responseOutput"
      ).textContent = `Response: ${result.message}`;
    } catch (error) {
      console.error("Error:", error);
      document.getElementById("responseOutput").textContent =
        "An error occurred.";
    }
  });
