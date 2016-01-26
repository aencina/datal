$( document ).ready( function( ) {

    $( '#id_confirmation_key_container' ).overlay(fOverlayDefaultsOptions);
    // usar un solo bind y decidir ahi

    $( '#id_try_button' ).bind( 'click', { }, onSuccessValidateUser );
});

function onErrorValidateUser( pResponse ) {
    jQuery.TwitterMessage( {
        type: 'error', message:
        pResponse.pMessage
    });
}

function onSuccessValidateUser( pResponse ) {
    // preventing multiple clicks
    $('#id_try_button').unbind( 'click');
    
    lUrl = "/manageDeveloper/create/";
    $( '#id_confirmation_key_container' ).data( "overlay" ).load( );
    
    $.ajax({
        url: lUrl,
        type:'GET',
        data: '',
        cache: false,
        dataType: 'json',
        success: function( pResponse ) {
            $('.key').html(pResponse.pApiKey);
            $('#id_try_button').bind( 'click', { }, onSuccessValidateUser );
        },
        error: onErrorValidateUser
    });
}
