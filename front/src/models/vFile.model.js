export const fileTypes = {
    FILE: "file",
    FOLDER: "folder"
}
export default class VFile {
    constructor({ id, parent_folder_id, name, content, created_at, is_folder, editable }) {
        this.file_id = id;
        this.parent = parent_folder_id || 'root';
        this.name = name || 'untitled_file';
        this.content = content;
        this.created_at = created_at || Date.now();
        this.type = is_folder ? fileTypes.FOLDER : fileTypes.FILE;
        this.editable = editable || false;
    }
}