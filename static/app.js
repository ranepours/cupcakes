const BASE_URL="http://localhost:5000/api";

// generate html based on passed data
const generateHTML = () => {
    return `
    <div data-cupcake-id=${cupcake.id}>
        <li> ${cupcake.flavor} | ${cupcake.size} | ${cupcake.rating}
            <button class="delete">X</button>
        </li>
        <img class="image" src=${cupcake.image} alt="No Photo Available">
    </div>
    `;
}

// show cupcakes
async function showCupcakes(){
    const res = await axios.get(`${BASE_URL}/cupcakes`);

    for(let data of res.data.cupcakes){
        let newCupcake = $(generateHTML(data));
        $("#cupcakes-list").append(newCupcake);
    }
}

//handle add new
$("new-cupcake").on("submit", async function(e){
    e.preventDefault();

    let flavor = $("flavor").val();
    let size = $("size").val();
    let image = $("image").val();
    let rating = $("rating").val();

    const resNewCupcake = await axios.post(`${BASE_URL}/cupcakes`, {
        flavor, size, rating, image
    });

    let newCupcake = $(generateHTML(resNewCupcake.data.cupcake));
    $("cupcakes-list").append(newCupcake);
    $("new-cupcake").trigger("reset");
})

//handle delete
$("cupcakes-list").on("click", ".delete", async function(e){
    e.preventDefault();
    let $cupcake = $(e.target).closest("div");
    let cupcakeID = $cupcake.attr("data-cupcake-id");

    await axios.delete(`${BASE_URL}/cupcakes/${cupcakeID}`);
    $cupcake.remove();
})

$(showCupcakes);