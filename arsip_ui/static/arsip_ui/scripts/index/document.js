document.addEventListener("DOMContentLoaded", function () {
    const dropArea = document.getElementById("drop-area");
    const fileInput = document.getElementById("file");
    const fileInfo = document.getElementById("file-info");
  
    dropArea.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropArea.classList.add("bg-gray-200");
    });
  
    dropArea.addEventListener("dragleave", () => {
        dropArea.classList.remove("bg-gray-200");
    });
  
    dropArea.addEventListener("drop", (e) => {
        e.preventDefault();
        dropArea.classList.remove("bg-gray-200");
  
        let files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
  
    dropArea.addEventListener("click", () => fileInput.click());
  
    fileInput.addEventListener("change", (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
  
    function handleFile(file) {
        if (file.type !== "application/pdf") {
            const isDarkMode = (localStorage.getItem('theme') === 'dark');
            Swal.fire({
                icon: "error",
                title: "Gagal",
                text: "File yang diupload harus berupa PDF",
                background: isDarkMode ? "#344C64" : "#fff",
                color: isDarkMode ? "#fff" : "#000"
            });
            fileInput.value = "";
            fileInfo.textContent = "";
            return;
        }
  
        fileInfo.textContent = `File yang dipilih: ${file.name}`;
  
        fileInput.files = new DataTransfer().files;
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }
  });
  
document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const submitButton = document.getElementById("submit-btn");
    const deleteButton = document.getElementById("delete-btn");
    const fileInput = document.getElementById("file");
    const dateInput = document.getElementById("tanggal-surat");
    const fileInfo = document.getElementById("file-info");

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();
        const existingFile = fileInfo && fileInfo.textContent.trim() !== "";
        const isDarkMode = (localStorage.getItem('theme') === 'dark');
        console.log(isDarkMode);

        let errorMessages = [];

        if (!dateInput.value && !fileInput.files.length) {
            errorMessages.push("Mohon isi kolom tanggal surat dan upload sebuah file");
        } else if (!dateInput.value) {
            errorMessages.push("Mohon isi kolom tanggal surat");
        } else if (!fileInput.files.length && !existingFile) {
            errorMessages.push("Mohon upload sebuah file");
        }

        if (errorMessages.length > 0) {
            Swal.fire({
                icon: "error",
                title: "Error",
                text: errorMessages.join(" \n"),
                background: isDarkMode ? "#344C64" : "#fff",
                color: isDarkMode ? "#fff" : "#000"
            });
            return;
        }

        Swal.fire({
            title: "Apakah Anda yakin?",
            text: "Pastikan data yang dimasukkan sudah benar",
            icon: "question",
            showCancelButton: true,
            confirmButtonColor: "#3085d6",
            cancelButtonColor: "#d33",
            confirmButtonText: "Simpan",
            cancelButtonText: "Batal",
            background: isDarkMode ? "#344C64" : "#fff",
            color: isDarkMode ? "#fff" : "#000"
        }).then((result) => {
            if (result.isConfirmed) {
                const currentPage = window.location.pathname;
                Swal.fire({
                    icon: "success",
                    title: "Sukses!",
                    text: currentPage.includes("ubah_dokumen") ? "Dokumen berhasil diubah!" : "Dokumen berhasil ditambahkan!",
                    showConfirmButton: false,
                    timer: 2000,
                    background: isDarkMode ? "#344C64" : "#fff",
                    color: isDarkMode ? "#fff" : "#000"
                }).then(() => {
                    const actionInput = document.createElement("input");
                    actionInput.type = "hidden";
                    actionInput.name = "action";
                    actionInput.value = "save";
                    form.appendChild(actionInput);

                    submitButton.disabled = true;

                    form.submit();
                });
            }
        });
    });

    deleteButton.addEventListener("click", function (event) {
        event.preventDefault();
        const isDarkMode = (localStorage.getItem('theme') === 'dark');
        Swal.fire({
            title: "Hapus Dokumen",
            text: "Dokumen yang dihapus tidak dapat dikembalikan",
            icon: "warning",
            showCancelButton: true,
            confirmButtonColor: "#d33",
            cancelButtonColor: "#3085d6",
            confirmButtonText: "Hapus",
            cancelButtonText: "Batal",
            background: isDarkMode ? "#344C64" : "#fff",
            color: isDarkMode ? "#fff" : "#000"
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire({
                    icon: "success",
                    title: "Terhapus!",
                    text: "Dokumen berhasil dihapus",
                    showConfirmButton: false,
                    timer: 2000,
                    background: isDarkMode ? "#344C64" : "#fff",
                    color: isDarkMode ? "#fff" : "#000"
                }).then(() => {
                    const actionInput = document.createElement("input");
                    actionInput.type = "hidden";
                    actionInput.name = "action";
                    actionInput.value = "delete";
                    form.appendChild(actionInput);
                    deleteButton.disabled = true;
                    form.submit();
                });
            }
        });
    });
});