Dropzone.autoDiscover = false;

function init() {
    let dz = new Dropzone("#dropzone", {
        url: "/",
        maxFiles: 1,
        addRemoveLinks: true,
        dictDefaultMessage: "Some Message",
        autoProcessQueue: false
    });
    
    dz.on("addedfile", function() {
        if (dz.files[1]!=null) {
            dz.removeFile(dz.files[0]);        
        }
    });

    dz.on("complete", function (file) {
        let imageData = file.dataURL;
        
        var url = "http://127.0.0.1:5000/classify_image";
		//var url = "api/classify_image";

        $.post(url, {
            image_data: file.dataURL
        },function(data, status) {
            /* 
            Below is a sample response if you have two faces in an image lets say virat and roger together.
            Most of the time if there is one person in the image you will get only one element in below array
            data = [
                {
                    class: "donald_trump",
                    class_probability: [91.56, 1.05, 12.67, 22.00, 4.5, 3.55,0.44 ],
                    class_dictionary: "angela_merkel": 0,
					"donald_trump": 1,
					"imran_khan": 2,
					"kim_jong-un": 3,
					"narendra_modi": 4,
					"vladimir_putin": 5,
					"xi_jinping": 6}
                },
                {
                    class: "imran_khan",
                    class_probability: [ 1.05, 12.67, 91.56, 22.00, 4.5, 3.55,0.44 ],
                    class_dictionary: "angela_merkel": 0,
					"donald_trump": 1,
					"imran_khan": 2,
					"kim_jong-un": 3,
					"narendra_modi": 4,
					"vladimir_putin": 5,
					"xi_jinping": 6}
                }
            ]
            */
            console.log(data);
			/* if data is not empty that means haarcascade did find face and eyes */
            if (!data || data.length==0) {
                $("#resultHolder").hide();
                $("#divClassTable").hide();                
                $("#error").show();
                return;
            }
            let Politicians = ["angela_merkel", "donald_trump", "imran_khan", "kim_jong-un", "narendra_modi", "vladimir_putin", "xi_jinping"];
            
            let match = null;
            let bestScore = -1;
            for (let i=0;i<data.length;++i) {
                let maxScoreForThisClass = Math.max(...data[i].class_probability);
                if(maxScoreForThisClass>bestScore) {
                    match = data[i];
                    bestScore = maxScoreForThisClass;
                }
            }
            if (match) {
                $("#error").hide();
                $("#resultHolder").show();
                $("#divClassTable").show();
                $("#resultHolder").html($(`[data-politician="${match.class}"`).html());
                let classDictionary = match.class_dictionary;
                for(let personName in classDictionary) {
                    let index = classDictionary[personName];
                    let proabilityScore = match.class_probability[index];
                    let elementName = "#score_" + personName;
                    $(elementName).html(proabilityScore);
                }
            }
            // dz.removeFile(file);            
        });
    });

    $("#submitBtn").on('click', function (e) {
        dz.processQueue();		
    });
}

$(document).ready(function() {
    console.log( "ready!" );
    $("#error").hide();
    $("#resultHolder").hide();
    $("#divClassTable").hide();

    init();
});