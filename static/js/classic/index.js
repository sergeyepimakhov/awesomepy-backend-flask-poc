import { observeMutations } from "./mutations.js"

$(document).ready(function() {
    observeMutations();

    // replace anchor-link
    $('a.anchor-link').html('<i class="fas fa-link"></i>');

    // replace button
    console.log('modifying the run button');
    // $('button.thebelab-run-button').html('<i class="fas fa-link"></i>');
    // $('button.thebelab-run-button').remove();

    // remove prompts
    $('div.prompt').remove();

    // on click select to unselected and back
    $('div.cell.code_cell').on('click', function(){
        $('div.cell.code_cell').removeClass('selected').addClass('unselected');
        $(this).removeClass('unselected').addClass('selected');
    });

    // TODO: on "Run" click jump to the next cell
    // $('div.cell.code_cell.selected').next().find('div.cell.code_cell').addClass('selected');

    // TODO: double click on output -> disable it
});