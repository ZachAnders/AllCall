function onload() {
	$.tablesorter.addWidget({ 
		id: "groupLocations", 
		format: function(table) { 
			sort_order = $(".headerSortDown,.headerSortUp")
			sort_by_location = true
			if (sort_order.length > 0 && sort_order[0].innerHTML != "Location")
				sort_by_location = false

			var active = false
			var last_val = ""
			 
			for(var i=0; i < table.tBodies[0].rows.length; i++) { 
				row = table.tBodies[0].rows[i]
				if (row.cells[5].innerHTML != last_val) {
					last_val = row.cells[5].innerHTML
					active = !active
				}
				if (sort_by_location && active) {
					$(row).addClass("active")
				} else {
					$(row).removeClass("active")
				}
			} 
		} 
	}); 
	$("#allcall_aps").tablesorter({
		debug: true,
		widgets: ["groupLocations"],
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

function get_customers() {

}
