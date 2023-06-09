const EDITORS = {
    primary: "PRIMARY",
    secondary: "SECONDARY",
};

export { EDITORS };

export default function initialState() {
    return {
        activeEditor: EDITORS.primary,
        openFiles: {
            [EDITORS.primary]: [],
            [EDITORS.secondary]: [],
        },
        activeFiles: {
            [EDITORS.primary]: null,
            [EDITORS.secondary]: null
        }
    };
}