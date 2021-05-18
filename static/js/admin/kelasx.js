$( document ).ready( function () {
    $( '#tambahDataKelas' ).on( 'click', function ( e ) {
        e.preventDefault();

        let namaKelas = $( '#namaKelas' ).val();
        let program = $( '#programKeahlian' ).val();
        let bidang = $( '#bidangKeahlian' ).val();
        let kelas = $( '#selectKelas' ).val();


        if ( namaKelas != "" && program != "" && bidang != "" && kelas != "" ) {
            $.ajax( {
                method: "POST",
                url: '/admin/input/kelasx',
                contentType: 'application/json;charset=UTF-8',
                data: JSON.stringify( { 'namaKelas': namaKelas, 'program': program, 'bidang': bidang, 'kelas': kelas } ),
                dataType: "json",
                success: function ( data ) {
                    if ( data.status == 200 ) {
                        swal( "Sukses", "Data Sudah Diinput", "success" ).then( ( value ) => {
                            location.reload();
                        } );
                    }
                },
                error: function ( err ) {
                    swal( "Gagal", "Data gagal diinput", "error" );
                }
            } );
        }
    } )
} );