document.addEventListener("DOMContentLoaded", function () {
    const fromAirport = document.getElementById("from_airport");
    const toAirport = document.getElementById("to_airport");

    function filterToAirportOptions() {
        const selectedFrom = fromAirport.value;

        // First, unhide all options
        for (let option of toAirport.options) {
            option.style.display = "block";
        }

        // Then hide the selected 'from' value in the 'to' list
        if (selectedFrom !== "") {
            for (let option of toAirport.options) {
                if (option.value === selectedFrom) {
                    option.style.display = "none";
                }
            }

            // If current 'to' value matches selected 'from', clear it
            if (toAirport.value === selectedFrom) {
                toAirport.value = "";
            }
        }
    }

    fromAirport.addEventListener("change", filterToAirportOptions);

    // Run on page load
    filterToAirportOptions();
});
