<template>
  <div class="container">
    <upload url="http://localhost:5000/api/files" multiple=true></upload>
    <MultiFileUpload/>
  </div>
</template>


<script>
import ApiService from '@/services/api.service';
const api = new ApiService('??')
import upload from '@/components/Admin/upload.vue';
import MultiFileUpload from '@/components/Admin/MultiFileUpload.vue';
export default {
    name: "FilesUpload",
    data() {
        return {
          uploadedFiles: [],
          fileProgress: 0,
          allFilesUploaded: false
        }
    },
    components: {
      upload,
      MultiFileUpload
    },
    computed: {
      fileProgress() {
        return {
          width: this.fileProgress
        }
      }
    },
    methods: {
        onFileClick(file) {
          console.log('onFileClick', file);
        },
        selectFile() {
            this.progressInfos = [];
            console.log(event.target.files);
            this.selectedFiles = event.target.files;
        },
        uploadFiles() {
        this.message = "";

            for (let i = 0; i < this.selectedFiles.length; i++) {
                console.log('САААЛМ', this.selectedFiles[i]);
                this.upload(i, this.selectedFiles[i]);
            }
        },
        upload(idx, file) {
            // api.upload('files', file);
            this.progressInfos[idx] = { percentage: 0, fileName: file.name };
            api.upload('files', file, (event) => {
                console.log('loaded:',event.loaded);
                console.log('total:', event.total)
                 this.progressInfos[idx].percentage = Math.round(100 * event.loaded / event.total);
             }).then((response) => {
                console.log('response;', response);
                let prevMessage = this.message ? this.message + "\n" : "";
                this.message = prevMessage + response.data.message;
             }).catch(() => {
                this.progressInfos[idx].percentage = 0;
                this.message = "Could not upload the file:" + file.name;
             })
            // //  UploadService.upload(file, (event) => {
            //      this.progressInfos[idx].percentage = Math.round(100 * event.loaded / event.total);
            //  })
            //      .then((response) => {
            //      let prevMessage = this.message ? this.message + "\n" : "";
            //      this.message = prevMessage + response.data.message;

            //      return UploadService.getFiles();
            //      })
            //      .then((files) => {
            //      this.fileInfos = files.data;
            //      })
            //      .catch(() => {
            //      this.progressInfos[idx].percentage = 0;
            //      this.message = "Could not upload the file:" + file.name;
            //      });
            }
    }
}
</script>

<style scoped>
.progress-bar {
  opacity: 1;
  height: 2px;
  margin: 0.4em 0;
  width: 0;
  background: green;
}

</style>