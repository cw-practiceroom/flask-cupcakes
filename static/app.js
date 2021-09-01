BASE_URL = 'http://127.0.0.1:5000/api';

deleteBtn = $('.delete-cupcake');
$('.delete-cupcake').on('click', removeCupcake);

async function removeCupcake() {
  const id = $(this).data('id');
  console.log('hello', id);
  await axios.delete(`${BASE_URL}/cupcakes/${id}`);
  $(this).parent().remove();
}
