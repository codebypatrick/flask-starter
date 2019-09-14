var d = document.querySelectorAll('.fromNow-date')
for (i=0; i < d.length; i++){
	var v = d[i].getAttribute('title');
	d[i].textContent = moment(v).fromNow();
}

var calendarDate =  document.querySelectorAll('.calendar-date');

for (i=0; i < calendarDate.length; i++) {
	var value = calendarDate[i].getAttribute('title');
	calendarDate[i].textContent = moment(value).calendar();
}

var ld = document.querySelectorAll('.long-date');

for (d=0; d < ld.length; d++) {
	var v = ld[d].getAttribute('title');
	ld[d].textContent = moment(v).format('ll');
}
