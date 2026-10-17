import streamlit as st

st.title("IndexedDB 技術検証")

memo = st.text_input(
    "保存する学習メモ",
    value="Pythonを60分勉強した"
)

delete_id = st.text_input("削除する記録のUUID")

edit_id = st.text_input("編集する記録のUUID")
edit_text = st.text_input("編集後の学習メモ")

JS = """
function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open("study_architect_poc_multi", 1);

        request.onupgradeneeded = () => {
            const db = request.result;

            if (!db.objectStoreNames.contains("memos")) {
                db.createObjectStore("memos", {keyPath: "id"});
            }
        };

        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function saveMemo(text) {
    const db = await openDatabase();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("memos", "readwrite");

        tx.objectStore("memos").put({
            id: crypto.randomUUID(),
            text: text
        });

        tx.oncomplete = () => {
            db.close();
            resolve();
        };

        tx.onabort = () => {
            db.close();
            reject(tx.error);
        };
    });
}

async function loadMemo() {
    const db = await openDatabase();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("memos", "readonly");
        const request = tx.objectStore("memos").getAll();

        tx.oncomplete = () => {
            db.close();
            resolve(request.result ?? []);
        };

        tx.onabort = () => {
            db.close();
            reject(tx.error);
        };
    });
}

async function deleteMemo(id) {
    const db = await openDatabase();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("memos", "readwrite");
        tx.objectStore("memos").delete(id)

        tx.oncomplete = () => {
            db.close();
            resolve();
        };

        tx.onabort = () => {
            db.close();
            reject(tx.error);
        } ;
    });
}

async function updateMemo(id, newText) {
    const db = await openDatabase();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("memos", "readwrite");
        const store = tx.objectStore("memos");

        const request = store.get(id);

        request.onsuccess = () => {
        const record = request.result;

            if (!record) {
                tx.abort();
                return;
            }

            store.put({
                ...record,
                text: newText
            });
        };

        tx.oncomplete = () => {
            db.close();
            resolve();
        };

        tx.onabort = () => {
            db.close();
            reject(new Error("UUIDが存在しないか、更新に失敗しました"));
        };
    });
}

export default function({ parentElement, data, setStateValue }) {
    const saveButton = parentElement.querySelector("#save");
    const loadButton = parentElement.querySelector("#load");
    const deleteButton = parentElement.querySelector("#delete");
    const updateButton = parentElement.querySelector("#update");
    const status = parentElement.querySelector("#status");

    saveButton.onclick = async () => {
        try {
            await saveMemo(data.memo);
            status.textContent = "IndexedDBへの保存成功";
        } catch (error) {
            status.textContent = "保存エラー: " + error.message;
        }
    };

    loadButton.onclick = async () => {
        try {
            const record = await loadMemo();

            status.textContent = "読み込み完了";
            setStateValue("restored", record);
        } catch (error) {
            status.textContent = "読み込みエラー: " + error.message;
        }
    };

    deleteButton.onclick = async () => {
        const id = data.delete_id.trim();

        if (!id) {
            status.textContent = "削除するUUIDを入力してください";
            return;
        }

        try {
            await deleteMemo(id);

            const records = await loadMemo();

            status.textContent = "削除処理が完了しました";
            setStateValue("restored", records);

        } catch (error) {
            status.textContent = "削除エラー: " + error.message;
        }
    }

    updateButton.onclick = async () => {
        const id = data.edit_id.trim();
        const text = data.edit_text.trim();

        if (!id || !text) {
            status.textContent = "UUIDと編集後のメモを入力してください";
            return;
        }

        try {
            await updateMemo(id, text);

            const records = await loadMemo();

            status.textContent = "編集が完了しました";
            setStateValue("restored", records);

        } catch (error) {
            status.textContent = "編集エラー: " + error.message;
        }
    };
};
"""

HTML = """
<div>
    <button id="save">ブラウザに保存</button>
    <button id="load">ブラウザから読み込み</button>
    <button id="delete">指定した記録を削除</button>
    <button id="update">指定した記録を編集</button>
    <p id="status"></p>
</div>
"""

storage_component = st.components.v2.component(
    "indexeddb_poc",
    html=HTML,
    js=JS
)

result = storage_component(
    data={"memo": memo,
          "delete_id": delete_id,
          "edit_text": edit_text,
          "edit_id": edit_id
    },
    key="storage_test",
    default={"restored": None},
    on_restored_change=lambda: None
)

if result.restored is not None:
    st.success("Pythonへのデータ復元成功")
    st.json(result.restored)