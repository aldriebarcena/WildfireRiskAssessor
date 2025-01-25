// Add an event listener to the button
document.getElementById('submitButton').addEventListener('click', function() {

    // Change the background color of the body when the button is clicked
    document.body.style.backgroundColor = '#ff5733';

    // Hide the first form (dataForm)
    document.getElementById('dataForm').style.display = 'none';
    // document.getElementById('dataForm').style.display = 'block';
  
    // Show the second form (changeBkg)
    document.getElementById('changeBkg').style.display = 'block';
    // document.getElementById('changeBkg').style.display = 'none';
  
});
  