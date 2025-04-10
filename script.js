async function checkSpam() {
  const message = document.getElementById("message").value;
  const resultDiv = document.getElementById("result");

  if (!message) {
    resultDiv.textContent = "Please enter a message.";
    return;
  }

  resultDiv.textContent = "Checking...";
  try {
    const response = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    const data = await response.json();
    if (response.ok) {
      resultDiv.textContent = `Prediction: ${data.prediction}`;
    } else {
      resultDiv.textContent = `Error: ${data.error}`;
    }
  } catch (error) {
    resultDiv.textContent = "An error occurred while checking the message.";
  }
}
