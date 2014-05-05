active_customers = []
function onload() {
	// Push all customers onto the list to begin with
	var rows = $("#customer_equips")[0].rows
	for (var i = 1; i < rows.length; i += 1) {
		active_customers.push(rows[i].cells[0].children[0].id);
	}

	//Setup the table sorter:
	$.tablesorter.addWidget({ 
		id: "groupAPs", 
		format: function(table) { 
			sort_order = $(".headerSortDown,.headerSortUp")
			sort_by_ap = true
			if (sort_order.length > 0 && sort_order[0].innerHTML != "Access Point ID")
				sort_by_ap = false

			var active = false
			var last_val = ""
			 
			for(var i=0; i < table.tBodies[0].rows.length; i++) { 
				row = table.tBodies[0].rows[i]
				if (row.cells[1].innerHTML != last_val) {
					last_val = row.cells[1].innerHTML
					active = !active
				}
				if (sort_by_ap && active) {
					$(row).addClass("active")
				} else {
					$(row).removeClass("active")
				}
			} 
		} 
	}); 
	$("#customer_equips").tablesorter({
		debug: true,
		widgets: ["groupAPs"],
		headers: {
			0:{
				sorter:false
			}
		}
	}); 
}


function toggle_customer(cust_id) {
	//$("#" + cust_id)
	cust_button = $("#" + cust_id)
	if (cust_button.hasClass("btn-danger")) {
		cust_button.removeClass("btn-danger")
		cust_button.addClass("btn-info")
		cust_button.text("Select")
	} else {
		cust_button.removeClass("btn-info")
		cust_button.addClass("btn-danger")
		cust_button.text("Remove")
	}
	cust_ind = active_customers.indexOf(cust_id)
	if (cust_ind != -1) {
		active_customers.splice(cust_ind, 1)
	} else {
		active_customers.push(cust_id)
	}
	console.log(JSON.stringify(active_customers))
}

function launch_allcall() {
	$("#selected_custs").val(JSON.stringify(active_customers))
	$("#customer_form").submit();
}
