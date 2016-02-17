$(document).ready(function(){

    var lHeaderSearchForm = new HeaderSearchForm();
    var lHeaderMenu = new HeaderMenu();
    
    var my_datatable_container = '#my_datatable';
    var my_datatable_selector = '#my_datatable';

    window.datatableHomeManager = new DatatableHomeManager({container: my_datatable_container, selector: my_datatable_selector, url: '/home/update_list/'});
    window.datatableHomeFilterManager = new DatatableHomeFilterManager({container: my_datatable_container, selector: '#home_filter' });
    window.datatableSearchManager = new DatatableSearchManager({container: my_datatable_container, selector: '#dataset_search' });
    window.datatablePaginationManager = new DatatablePaginationManager({container: my_datatable_container, selector: '#home_pagination' });
    window.datatableHeaderManager = new DatatableHomeHeaderManager({container: my_datatable_container, selector: '#resources_header', clickable_columns: ['0', '1']});  

}); 