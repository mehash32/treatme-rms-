let ratedIndex = -1;

$(document).ready(function(){
    const star = $('.review');
    
    resetColor();

    $(star).click(function(){
        ratedIndex =  parseInt($(this).data('index'));
        console.log(parseInt(ratedIndex));
        $("#rating").val(ratedIndex);
    })

    $(star).mouseover(function(){
        let current = parseInt($(this).data('index'));

        setStarColor(current);
    });

    $(star).mouseleave(function(){
        resetColor();

        if(ratedIndex != -1){
            setStarColor(ratedIndex);
        }
    });

    function resetColor(){
        $(star).css('color', '#cfd8dc');
    }

    function setStarColor(max){
        for(let i=0; i<max; i++){
            $(star[i]).css('color', '#fbc02d');
        }
    }
});
