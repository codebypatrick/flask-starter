//parse dates
//TODO friendly dates ie 3m ago
var nowElements = document.getElementsByClassName('.moment');

for(var i = 0; i < nowElements.length; ++i) {
	var item = nowElements[i];
	var displayDate = nowElements[i].getAttribute('title');
	var dt = moment(displayDate).format('ll')
	item.innerHTML = dt;
}
