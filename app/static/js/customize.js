document.addEventListener("DOMContentLoaded", () => {
    const addTextBtn = document.getElementById("addTextBtn");
    const addLogoBtn = document.getElementById("addLogoBtn");
    const previewArea = document.getElementById("previewArea");
    const logoUploader = document.createElement("input");
    logoUploader.type = "file";
    logoUploader.accept = "image/*";

    // Function to add text
    addTextBtn.addEventListener("click", () => {
        const textElement = document.createElement("div");
        textElement.textContent = "New Text";
        textElement.style.position = "absolute";
        textElement.style.left = "50px";
        textElement.style.top = "50px";
        textElement.style.fontSize = "16px";
        textElement.style.color = "#000";
        textElement.style.fontFamily = "Arial";
        textElement.contentEditable = true;
        textElement.classList.add("custom-text", "draggable");

        // Add drag functionality
        enableDrag(textElement);
        previewArea.appendChild(textElement);
    });

    // Function to add logo
    addLogoBtn.addEventListener("click", () => {
        logoUploader.click(); // Trigger file upload dialog
    });

    logoUploader.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const imgElement = document.createElement("img");
            imgElement.src = URL.createObjectURL(file);
            imgElement.style.position = "absolute";
            imgElement.style.left = "100px";
            imgElement.style.top = "100px";
            imgElement.style.width = "100px";
            imgElement.style.cursor = "move";
            imgElement.classList.add("custom-logo", "draggable");

            // Add drag functionality
            enableDrag(imgElement);
            previewArea.appendChild(imgElement);
        }
    });

    // Function to enable drag functionality
    function enableDrag(element) {
        let isDragging = false;
        let offsetX = 0;
        let offsetY = 0;

        element.addEventListener("mousedown", (e) => {
            isDragging = true;
            const rect = element.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;

            document.addEventListener("mousemove", onMouseMove);
            document.addEventListener("mouseup", onMouseUp);
        });

        function onMouseMove(e) {
            if (isDragging) {
                const rect = previewArea.getBoundingClientRect();
                const newX = e.clientX - rect.left - offsetX;
                const newY = e.clientY - rect.top - offsetY;

                element.style.left = `${newX}px`;
                element.style.top = `${newY}px`;
            }
        }

        function onMouseUp() {
            isDragging = false;
            document.removeEventListener("mousemove", onMouseMove);
            document.removeEventListener("mouseup", onMouseUp);
        }
    }

    // Attach the save function to a button
    document.getElementById("save-button").addEventListener("click", saveCustomizations);

    // Save customization function
    function saveCustomizations() {
        const customizationData = {
            text: [],
            logos: []
        };

        // Extract text elements
        document.querySelectorAll(".custom-text").forEach((textElement) => {
            customizationData.text.push({
                content: textElement.textContent,
                fontSize: window.getComputedStyle(textElement).fontSize,
                fontFamily: window.getComputedStyle(textElement).fontFamily,
                color: window.getComputedStyle(textElement).color,
                position: {
                    x: textElement.style.left,
                    y: textElement.style.top
                }
            });
        });

        // Extract logo elements
        document.querySelectorAll(".custom-logo").forEach((logoElement) => {
            customizationData.logos.push({
                src: logoElement.src,
                position: {
                    x: logoElement.style.left,
                    y: logoElement.style.top
                },
                size: {
                    width: logoElement.style.width,
                    height: logoElement.style.height
                }
            });
        });

        // Send the data to the server
        fetch("/customize/save_customizations", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(customizationData),
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json(); // Parse JSON if the response is OK
            })
            .then((data) => {
                if (data.message) {
                    alert("Customizations saved successfully!");
                } else {
                    alert("Failed to save customizations.");
                }
            })
            .catch((error) => {
                console.error("Error:", error);
                alert("An error occurred while saving customizations.");
            });        
    }
});



