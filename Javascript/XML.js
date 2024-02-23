<script>
        // DISPLAY ALL FETCHED EXTERNAL PSGC API
        document.addEventListener("DOMContentLoaded", function() {
            showMindanaoRegions();
            showVisayasRegions();
            showLuzonRegions();
            showMunicipalities();
        });

        //SHOW MUNICIPALITIES DROPDOWN------------------------------
        function showMunicipalities() {
            let xhr = new XMLHttpRequest();

            xhr.open('GET', 'https://psgc.gitlab.io/api/municipalities/', true);

            xhr.onload = function() {
                if (xhr.status == 200) {
                    console.log('success');
                    let municipalities = JSON.parse(this.response);

                    // Log municipalities to the console
                    console.log(municipalities);

                    // Get the dropdown element
                    const municipalitiesDropdown = document.getElementById('municipalitiesDropdown');

                    // Clear existing options
                    municipalitiesDropdown.innerHTML = "";

                    // Populate the dropdown with regions
                    municipalities.forEach(municipality => {
                        const option = document.createElement('option');
                        option.value = municipality.name;
                        option.text = municipality.name;
                        municipalitiesDropdown.appendChild(option);
                    });
                }
            };
            xhr.send();
        }

       //SHOW LUZON REGION DROPDOWN------------------------------
        function showLuzonRegions() {
            let xhr = new XMLHttpRequest();

            xhr.open('GET', 'https://psgc.gitlab.io/api//island-groups/luzon/regions/', true);

            xhr.onload = function() {
                if (xhr.status == 200) {
                    console.log('success');
                    let regions = JSON.parse(this.response);

                    // Log regions to the console
                    console.log(regions);

                    // Get the dropdown element
                    const luzonRegionDropdown = document.getElementById('luzonRegionDropdown');

                    // Clear existing options
                    luzonRegionDropdown.innerHTML = "";

                    // Populate the dropdown with regions
                    regions.forEach(region => {
                        const option = document.createElement('option');
                        option.value = region.name;
                        option.text = region.name;
                        luzonRegionDropdown.appendChild(option);
                    });
                }
            };
            xhr.send();
        }

        //SHOW VISAYAS REGION DROPDOWN------------------------------
        function showVisayasRegions() {
            let xhr = new XMLHttpRequest();

            xhr.open('GET', 'https://psgc.gitlab.io/api//island-groups/visayas/regions/', true);

            xhr.onload = function() {
                if (xhr.status == 200) {
                    console.log('success');
                    let regions = JSON.parse(this.response);

                    // Log regions to the console
                    console.log(regions);

                    // Get the dropdown element
                    const visayasRegionDropdown = document.getElementById('visayasRegionDropdown');

                    // Clear existing options
                    visayasRegionDropdown.innerHTML = "";

                    // Populate the dropdown with regions
                    regions.forEach(region => {
                        const option = document.createElement('option');
                        option.value = region.name;
                        option.text = region.name;
                        visayasRegionDropdown.appendChild(option);
                    });
                }
            };
            xhr.send();
        }

        //SHOW MINDANAO REGION DROPDOWN------------------------------
        function showMindanaoRegions() {
            let xhr = new XMLHttpRequest();

            xhr.open('GET', 'https://psgc.gitlab.io/api//island-groups/mindanao/regions/', true);

            xhr.onload = function() {
                if (xhr.status == 200) {
                    console.log('success');
                    let regions = JSON.parse(this.response);

                    // Log regions to the console
                    console.log(regions);

                    // Get the dropdown element
                    const mindanaoRegionDropdown = document.getElementById('mindanaoRegionDropdown');

                    // Clear existing options
                    luzonRegionDropdown.innerHTML = "";

                    // Populate the dropdown with regions
                    regions.forEach(region => {
                        const option = document.createElement('option');
                        option.value = region.name;
                        option.text = region.name;
                        mindanaoRegionDropdown.appendChild(option);
                    });
                }
            };
            xhr.send();
        }
    </script>