// Define the result object with a percentage value
const result = { percentage: 90 }; // Example result object

document
  .getElementById("submitButton")
  .addEventListener("click", async (event) => {
    event.preventDefault(); // Prevent form from submitting
    // Hide the first form (dataForm)
    document.getElementById("dataForm").style.display = "none";

    // Show the second form (changeBkg)
    document.getElementById("changeBkg").style.display = "block";

    // update percentage
    const percentage = document.getElementById("percentage");
    percentage.textContent = `${result.percentage}%`;

    // change background color based on percentage
    const body = document.body;

    // Add the background color change logic
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
  });
