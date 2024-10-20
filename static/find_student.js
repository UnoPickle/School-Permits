const studentInputId = 'student-search';
const searchResultsId = 'search-results'

const requestServer = '127.0.0.1:5000'
const studentNamesUrlGetRequest = 'student_names'
const studentNameGetRequestParam = 'name'

async function searchName() {
    const student = document.getElementById(studentInputId).value

    let results = [];



    var a = 5;


    try {
        const response = await fetch(`http://${requestServer}/${studentNamesUrlGetRequest}?${studentNameGetRequestParam}=${student}`)
        results = await response.json();
    } catch (error) {
        console.error('Error: ', error)
    }

    let search_results_element = document.getElementById(searchResultsId);

    let child = search_results_element.lastElementChild;
    while (child) {
        search_results_element.removeChild(child)
        child = search_results_element.lastElementChild;
    }

    for (let result_index = 0; result_index < results.length; result_index++)
    {
        var result_option = document.createElement("button");
        result_option.appendChild(document.createTextNode(results[result_index]));
        result_option.setAttribute("class", "result_option");


        search_results_element.appendChild(result_option);
    }
}
