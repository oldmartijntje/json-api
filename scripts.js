
        function timeSince(date) {
            const seconds = Math.floor((new Date() - date) / 1000);
            let interval = Math.floor(seconds / 31536000);

            if (interval >= 1) {
                return interval + " year" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 2592000);
            if (interval >= 1) {
                return interval + " month" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 86400);
            if (interval >= 1) {
                return interval + " day" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 3600);
            if (interval >= 1) {
                return interval + " hour" + (interval > 1 ? "s" : "");
            }
            interval = Math.floor(seconds / 60);
            if (interval >= 1) {
                return interval + " minute" + (interval > 1 ? "s" : "");
            }
            return Math.floor(seconds) + " second" + (seconds > 1 ? "s" : "");
        }

        function updateTimeSince() {
            const elements = document.querySelectorAll('.time-since');
            elements.forEach(element => {
                const datetimeString = element.getAttribute('data-value');
                const datetime = new Date(datetimeString);
                element.textContent = timeSince(datetime) + " ago";
            });
        }

        // Initial update
        updateTimeSince();

        // Update every 10 seconds
        setInterval(updateTimeSince, 10000);

        document.querySelectorAll('input[name="view"]').forEach((radio) => {
            radio.addEventListener('change', (event) => {
                handleRadioChange(event.target.id);
            });
        });

        function handleRadioChange(selectedId) {
            if (selectedId === 'listView') {
                console.log('List View selected');
                // Add your code to handle List View selection
                document.getElementById('list').style.display = 'block';
                document.getElementById('icon').style.display = 'none';
            } else if (selectedId === 'iconView') {
                console.log('Icon View selected');
                document.getElementById('list').style.display = 'none';
                document.getElementById('icon').style.display = 'block';

                // Add your code to handle Icon View selection
            }
        }
        handleRadioChange('iconView');

        document.addEventListener("DOMContentLoaded", function () {
            const lazyImages = document.querySelectorAll('img.lazy');

            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    } else {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = '';
                        }
                    }
                });
            });

            lazyImages.forEach(img => {
                imageObserver.observe(img);
            });
        });
        