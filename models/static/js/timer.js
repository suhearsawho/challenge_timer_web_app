/* Declare Variables */
var minutes = document.getElementById("minutes");
var seconds = document.getElementById("seconds");

/* Timer Function */
function countdown(time) {
	let time_left = time * 60;
	let timer_clock = setInterval(inCountdown, 1000);
	function inCountdown() {
		let minutes_value = Math.floor((time_left / 60));
		let seconds_value = Math.floor((time_left % 60));
		
		if (seconds_value < 10)
			seconds_value = '0' + seconds_value;
		minutes.innerHTML = minutes_value;
		seconds.innerHTML = seconds_value;
		if (time_left == 0)
		{
			clearInterval(timer_clock);
		}
		else
		{
			time_left = time_left - 1;
		}
	}
}
