import streamlit as st
from analytics import (
    calculate_total_minutes,
    calculate_subject_totals
)
from ui.overview_tab import render_overview_tab
from ui.detail_tab import render_detail_tab

RECORD_HTML = """
<div>
    <button id="save-record">学習記録を保存</button>
    <button id="load-records">学習記録を読み込む</button>
    <p id="record-status"></p>
</div>
"""

RECORD_JS = """
function openRecordsDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(
            "study_architect_records_poc", 1
        );

        request.onupgradeneeded = () => {
            const db = request.result;

            if (!db.objectStoreNames.contains("records")) {
                db.createObjectStore("records", {
                    keyPath: "id"
                });
            }
        };

        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
    });
}

async function saveStudyRecord(record) {
    const db = await openRecordsDB();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("records", "readwrite");

        tx.objectStore("records").put({
            id: record.id ?? crypto.randomUUID(),
            date: record.date,
            subject: record.subject,
            minutes: record.minutes
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

async function loadStudyRecords() {
    const db = await openRecordsDB();

    return new Promise((resolve, reject) => {
        const tx = db.transaction("records", "readonly");
        const request = tx.objectStore("records").getAll();

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

export default function({ parentElement, data, setStateValue }) {
    const saveButton = parentElement.querySelector("#save-record");
    const loadButton = parentElement.querySelector("#load-records");
    const status = parentElement.querySelector("#record-status");

    function publish(records, action = null, error = null) {
        setStateValue("snapshot", { records, action, error });
    }

    saveButton.onclick = async () => {
        try {
            if (!data.record.subject.trim()) {
                status.textContent = "科目名を入力してください";
                return;
            }
            await saveStudyRecord(data.record);
            const records = await loadStudyRecords();
            status.textContent = "テスト記録を保存しました";
            publish(records);
        } catch (error) {
            status.textContent = "保存エラー: " + error.message;
        }
    };

    loadButton.onclick = async () => {
        try {
            const records = await loadStudyRecords();
            status.textContent = "読み込み成功";
            publish(records);
        } catch (error) {
            status.textContent = "読み込みエラー: " + error.message;
            publish(null, null, error.message);
        }
    };

    if (status.dataset.initialLoad !== "started") {
        status.dataset.initialLoad = "started";
        loadStudyRecords()
            .then(records => {
                status.textContent = "自動読み込み成功";
                publish(records);
            })
            .catch(error => {
                status.textContent = "自動読み込み失敗: " + error.message;
                publish(null, null, error.message);
            });
    }

    const command = data.pending_record;
    if (command) {
        const attemptKey = `${command.id}:${command.attempt}`;
        if (status.dataset.lastSaveAttempt !== attemptKey) {
            status.dataset.lastSaveAttempt = attemptKey;

            (async () => {
                try {
                    await saveStudyRecord(command);
                    const records = await loadStudyRecords();
                    publish(records, {
                        id: command.id,
                        attempt: command.attempt,
                        ok: true
                    });
                } catch (error) {
                    const records = await loadStudyRecords().catch(() => null);
                    publish(records, {
                        id: command.id,
                        attempt: command.attempt,
                        ok: false,
                        error: error.message
                    });
                }
            })();
        }
    }
}

"""

record_storage_component = st.components.v2.component(
    "study_records_preview",
    html=RECORD_HTML,
    js=RECORD_JS
)


def render_record_storage_preview(pending_record=None):
    study_date = st.date_input("学習日（IndexedDBテスト）")
    subject = st.text_input(
        "科目（IndexedDBテスト）",
        value="Python"
    )
    minutes = st.number_input(
        "学習時間（分・IndexedDBテスト）",
        min_value=1,
        value=60,
        step=1
    )

    result = record_storage_component(
        data={
            "record": {
                "date": study_date.isoformat(),
                "subject": subject,
                "minutes": minutes,
            },
            "pending_record": pending_record
        },
        key="study_records_preview",
        default={"snapshot": None},
        on_snapshot_change=lambda: None,
    )

    snapshot = result.snapshot
    if snapshot is None:
        return None

    if snapshot.get("error"):
        st.error(f"IndexedDBの読み込みに失敗しました: {snapshot["error"]}")

    action = snapshot.get("action")
    if (
        pending_record is not None
        and action is not None
        and action["id"] == pending_record["id"]
        and action["attempt"] == pending_record["attempt"]
    ):
        if action["ok"]:
            st.session_state["pending_record"] = None
            st.session_state["save_success"] = True
            st.rerun()
        else:
            st.error(f"IndexedDBへの保存に失敗しました: {action["erro"]}")
            if st.button("同じ記録を再試行", key="retry_browser_save"):
                st.session_state["pending_record"]["attempt"] += 1
                st.rerun()

    records = snapshot.get("records")
    if records is not None:
        st.json(records)
        st.metric("総勉強時間", f"{calculate_total_minutes(records)}分")
        st.bar_chart(calculate_subject_totals(records))
        st.divider()
        st.subheader("IndexedDB分析画面テスト")
        period = st.selectbox(
            "表示期間（テスト）",
            ["1週間", "1か月", "1年", "全期間"],
            key="indexeddb_period",
        )
        overview_tab, detail_tab = st.tabs(["概要", "詳細分析"])
        with overview_tab:
            render_overview_tab(records, period)
        with detail_tab:
            render_detail_tab(records)

    return records
