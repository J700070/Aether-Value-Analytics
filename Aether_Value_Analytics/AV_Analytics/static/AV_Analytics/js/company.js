function tabs(class_id) {
    const tab_list = ["Overview","Income_Statement", "Balance_Sheet", "Cash_Flow_Statement"];


    // Check valid id
    if (tab_list.includes(class_id)) {


        // Set tab as active
        document.getElementById(class_id).classList.add('active');

        // Change other tabs to normal
        for(let i = 0; i < tab_list.length; i++) {
            if (tab_list[i] !== class_id) {
                document.getElementById(tab_list[i]).classList.remove('active');
            }
        }



        // Change tab content
        // ================================================
        // Make new content visible
        var vis_elems = document.getElementsByClassName(class_id)

        for(let i = 0; i < vis_elems.length; i++) {
            vis_elems[i].style.display = "block";
        }

        // Hide old content
        for (let i = 0; i < tab_list.length; i++) {
            if (tab_list[i] !== class_id) {
                var non_vis_elems = document.getElementsByClassName(tab_list[i])
        
                for(let j = 0; j < non_vis_elems.length; j++) {
                    non_vis_elems[j].style.display = "none";
                }
            }
        }
        // ================================================
    }else{
        alert("Invalid Tab class_id");
    }
}