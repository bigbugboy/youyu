const deleteBtnList = document.getElementsByClassName('deleteBtn')


for (let index = 0; index < deleteBtnList.length; index++) {
    deleteBtnList[index].addEventListener('click', confirmDelete)
}


function confirmDelete(e) {
    let expenseId = e.target.getAttribute('expenseID')
    Swal.fire({
        title: "您确定删除这个记录吗?",
        text: "",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "删除!",
        cancelButtonText: "取消"
    }).then((result) => {
        if (result.isConfirmed) {
            handleDelete(expenseId)
        }
    })
}

function handleDelete(id) {
    fetch(`/expense/delete-expense/${id}`).then((data) => {
        location.reload()
    })
}