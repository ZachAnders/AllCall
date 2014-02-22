function oncall() {
	$("#allcall_aps").tablesorter({
		debug: true,
		headers: {
			0:{
				sorter:false
			},
			3:{
				sorter:"ipAddress"
			}
		}
	}); 
}

active_aps = []

function toggle_ap(ap_id) {
	//$("#" + ap_id)
	ap_button = $("#" + ap_id)
	if (ap_button.hasClass("btn-danger")) {
		ap_button.removeClass("btn-danger")
		ap_button.addClass("btn-info")
		ap_button.text("Remove")
	} else {
		ap_button.removeClass("btn-info")
		ap_button.addClass("btn-danger")
		ap_button.text("Select")
	}
	ap_ind = active_aps.indexOf(ap_id)
	if (ap_ind != -1) {
		active_aps.splice(ap_ind, 1)
	} else {
		active_aps.push(ap_id)
	}
	console.log(JSON.stringify(active_aps))
}
