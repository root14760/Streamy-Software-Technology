import io
import contextlib
import tkinter as tk
from tkinter import ttk, messagebox
from streamy_core import Film, TVShow, Season, Episode, Actor, Genre

TEXTS = {
    "en": {
        "win_title": "Streamy — Minimalist Runtime GUI",
        "header": "Streamy Platform",
        "lang_btn": "中文",
        "reset_btn": "Reset",
        "sec_media": "Media & Token Playback",
        "play_btn": "▶ Play",
        "status_wait": "Ready to verify playback token",
        "status_ok": "200 OK — HLS Stream Authorized",
        "status_fail": "401 Unauthorized — Access Denied",
        "sec_review": "User Reviews (Composition)",
        "review_placeholder": "Smooth 4K playback!",
        "add_btn": "+ Add",
        "empty_warn_title": "Notice",
        "empty_warn_msg": "Please enter review content first.",
        "sec_mem": "Lifecycle Constraints (Composition vs. Aggregation)",
        "purge_btn": "Purge Child Data (Cascade Delete)",
        "sec_log": "Core Engine Trace (streamy_core.py)",
        "tv_meta": "TVShow  |  {year}  |  Network: {net}",
        "film_meta": "Film  |  {year}  |  Duration: {mins} mins",
        "mem_stats": "Seasons (Composition): {s}    Reviews (Composition): {r}    Actors (Aggregation): {a} [Intact]",
        "log_review": "[Review] Added {stars}★ review to '{name}'.",
        "log_film_purge": "[Memory] Purged reviews for '{name}'. Actors kept intact: {a}.",
        "log_reset": "--- State reset to initial snapshot ---",
    },
    "zh": {
        "win_title": "Streamy — 架构验证精简界面",
        "header": "Streamy 流媒体平台",
        "lang_btn": "English",
        "reset_btn": "重置",
        "sec_media": "媒体选择与 Token 鉴权播放",
        "play_btn": "▶ 播放测试",
        "status_wait": "等待发起播放鉴权请求",
        "status_ok": "200 OK — 鉴权通过，已获取 HLS 视频流",
        "status_fail": "401 Unauthorized — Token 无效，拒绝播放",
        "sec_review": "用户影评（Composition 组合关系）",
        "review_placeholder": "画质清晰，播放流畅！",
        "add_btn": "+ 添加",
        "empty_warn_title": "提示",
        "empty_warn_msg": "请先输入影评内容。",
        "sec_mem": "生命周期约束（组合级联删除 vs 聚合保留）",
        "purge_btn": "触发级联删除（清理子对象数据）",
        "sec_log": "后端核心运行日志 (streamy_core.py)",
        "tv_meta": "电视剧 (TVShow)  |  {year}年  |  平台: {net}",
        "film_meta": "电影 (Film)  |  {year}年  |  时长: {mins} 分钟",
        "mem_stats": "季数 [组合]: {s}    影评 [组合]: {r}    演员 [聚合]: {a} (完整保留)",
        "log_review": "[影评服务] 已为《{name}》添加 {stars}★ 影评。",
        "log_film_purge": "[内存管理] 已清空《{name}》的影评；聚合关联的 {a} 名演员完整保留。",
        "log_reset": "--- 系统数据已重置为初始状态 ---",
    },
}


class StreamyAppGUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.lang = "en"
        self.auth_state = "wait"  # "wait" | "ok" | "fail"
        self.titles = {}
        self.current_title = None

        self.root.geometry("560x640")
        self.root.configure(bg="#f1f5f9")
        self.root.resizable(False, False)

        self._init_data()
        self._build_ui()
        self._apply_language()

    def _init_data(self):
        a1 = Actor("Ashley Peacock")
        a2 = Actor("Eddy Gerbil")
        a3 = Actor("Leonardo DiCaprio")

        genre = Genre("Sci-Fi")

        show = TVShow("Stranger Things", 2016, "Netflix")
        s1 = Season(1)
        s1.add_episode(Episode("Chapter One: The Vanishing of Will Byers", 2880))
        s2 = Season(2)
        s2.add_episode(Episode("Chapter One: MADMAX", 2900))
        show.add_season(s1)
        show.add_season(s2)
        show.link_actor(a1)
        show.link_actor(a2)
        show.add_review(5, "Classic retro sci-fi mystery!")

        film = Film("Inception", 2010, 148)
        film.link_actor(a3)
        film.link_actor(a1)
        film.add_review(5, "Mind-bending architecture!")

        genre.register_title(show)
        genre.register_title(film)

        self.titles = {
            "Stranger Things (TVShow)": show,
            "Inception (Film)": film,
        }
        self.current_title = show

    def _card(self, parent):
        frame = tk.Frame(parent, bg="#ffffff", padx=14, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
        frame.pack(fill=tk.X, pady=(0, 10))
        return frame

    def _build_ui(self):
        # Top Navigation Bar
        top = tk.Frame(self.root, bg="#0f172a", padx=16, pady=10)
        top.pack(fill=tk.X)

        self.lbl_header = tk.Label(top, font=("Segoe UI", 12, "bold"), fg="#ffffff", bg="#0f172a")
        self.lbl_header.pack(side=tk.LEFT)

        self.btn_reset = tk.Button(
            top, command=self._reset_all, bg="#334155", fg="#f8fafc",
            font=("Segoe UI", 9), relief=tk.FLAT, padx=10, pady=2, cursor="hand2"
        )
        self.btn_reset.pack(side=tk.RIGHT)

        self.btn_lang = tk.Button(
            top, command=self._toggle_language, bg="#2563eb", fg="#ffffff",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=2, cursor="hand2"
        )
        self.btn_lang.pack(side=tk.RIGHT, padx=(0, 8))

        # Main Content Container
        body = tk.Frame(self.root, bg="#f1f5f9", padx=14, pady=12)
        body.pack(fill=tk.BOTH, expand=True)

        # Card 1: Media & Playback
        c1 = self._card(body)
        self.lbl_sec_media = tk.Label(c1, font=("Segoe UI", 9, "bold"), fg="#334155", bg="#ffffff", anchor="w")
        self.lbl_sec_media.pack(fill=tk.X, pady=(0, 6))

        self.media_var = tk.StringVar(value="Stranger Things (TVShow)")
        cb_media = ttk.Combobox(c1, textvariable=self.media_var, values=list(self.titles.keys()), state="readonly", font=("Segoe UI", 9))
        cb_media.pack(fill=tk.X)
        cb_media.bind("<<ComboboxSelected>>", lambda e: self._on_media_change())

        self.lbl_meta = tk.Label(c1, font=("Segoe UI", 8), fg="#64748b", bg="#ffffff", anchor="w")
        self.lbl_meta.pack(fill=tk.X, pady=(3, 8))

        row_auth = tk.Frame(c1, bg="#ffffff")
        row_auth.pack(fill=tk.X)

        self.token_var = tk.StringVar(value="VALID_STREAM_TOKEN_2026")
        ttk.Combobox(
            row_auth, textvariable=self.token_var,
            values=["VALID_STREAM_TOKEN_2026", "EXPIRED_TOKEN", ""], font=("Segoe UI", 9)
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        self.btn_play = tk.Button(
            row_auth, command=self._handle_play, bg="#2563eb", fg="#ffffff",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=12, pady=2, cursor="hand2"
        )
        self.btn_play.pack(side=tk.RIGHT)

        self.lbl_status = tk.Label(c1, font=("Segoe UI", 8, "bold"), bg="#ffffff", anchor="w")
        self.lbl_status.pack(fill=tk.X, pady=(6, 0))

        # Card 2: Reviews
        c2 = self._card(body)
        self.lbl_sec_review = tk.Label(c2, font=("Segoe UI", 9, "bold"), fg="#334155", bg="#ffffff", anchor="w")
        self.lbl_sec_review.pack(fill=tk.X, pady=(0, 6))

        row_rev = tk.Frame(c2, bg="#ffffff")
        row_rev.pack(fill=tk.X, pady=(0, 6))

        self.rating_var = tk.IntVar(value=5)
        ttk.Combobox(row_rev, textvariable=self.rating_var, values=[5, 4, 3, 2, 1], width=3, state="readonly").pack(side=tk.LEFT, padx=(0, 6))

        self.entry_review = tk.Entry(row_rev, font=("Segoe UI", 9), relief=tk.SOLID, borderwidth=1)
        self.entry_review.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 6))

        self.btn_add = tk.Button(
            row_rev, command=self._handle_add_review, bg="#059669", fg="#ffffff",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, padx=10, pady=1, cursor="hand2"
        )
        self.btn_add.pack(side=tk.RIGHT)

        self.list_reviews = tk.Listbox(c2, height=2, font=("Segoe UI", 8), bg="#f8fafc", relief=tk.FLAT, highlightthickness=1, highlightbackground="#e2e8f0")
        self.list_reviews.pack(fill=tk.X)

        # Card 3: Lifecycle Memory
        c3 = self._card(body)
        self.lbl_sec_mem = tk.Label(c3, font=("Segoe UI", 9, "bold"), fg="#334155", bg="#ffffff", anchor="w")
        self.lbl_sec_mem.pack(fill=tk.X, pady=(0, 4))

        self.lbl_stats = tk.Label(c3, font=("Consolas", 8, "bold"), fg="#0f172a", bg="#ffffff", anchor="w")
        self.lbl_stats.pack(fill=tk.X, pady=(0, 8))

        self.btn_purge = tk.Button(
            c3, command=self._handle_purge, bg="#dc2626", fg="#ffffff",
            font=("Segoe UI", 9, "bold"), relief=tk.FLAT, pady=4, cursor="hand2"
        )
        self.btn_purge.pack(fill=tk.X)

        # Card 4: Compact Runtime Log
        c4 = tk.Frame(body, bg="#ffffff", padx=14, pady=10, highlightbackground="#e2e8f0", highlightthickness=1)
        c4.pack(fill=tk.BOTH, expand=True)

        self.lbl_sec_log = tk.Label(c4, font=("Segoe UI", 9, "bold"), fg="#334155", bg="#ffffff", anchor="w")
        self.lbl_sec_log.pack(fill=tk.X, pady=(0, 4))

        self.txt_log = tk.Text(c4, height=7, font=("Consolas", 8), bg="#0f172a", fg="#e2e8f0", wrap=tk.WORD, state=tk.DISABLED, padx=8, pady=6)
        self.txt_log.pack(fill=tk.BOTH, expand=True)

    def _t(self, key: str) -> str:
        return TEXTS[self.lang][key]

    def _toggle_language(self):
        self.lang = "zh" if self.lang == "en" else "en"
        self._apply_language()

    def _apply_language(self):
        self.root.title(self._t("win_title"))
        self.lbl_header.config(text=self._t("header"))
        self.btn_lang.config(text=self._t("lang_btn"))
        self.btn_reset.config(text=self._t("reset_btn"))
        self.lbl_sec_media.config(text=self._t("sec_media"))
        self.btn_play.config(text=self._t("play_btn"))
        self.lbl_sec_review.config(text=self._t("sec_review"))
        self.btn_add.config(text=self._t("add_btn"))
        self.lbl_sec_mem.config(text=self._t("sec_mem"))
        self.btn_purge.config(text=self._t("purge_btn"))
        self.lbl_sec_log.config(text=self._t("sec_log"))

        self.entry_review.delete(0, tk.END)
        self.entry_review.insert(0, self._t("review_placeholder"))
        self._refresh_views()

    def _refresh_views(self):
        t = self.current_title
        if isinstance(t, TVShow):
            self.lbl_meta.config(text=self._t("tv_meta").format(year=t.release_year, net=t.network))
        else:
            self.lbl_meta.config(text=self._t("film_meta").format(year=t.release_year, mins=t.length_minutes))

        status_map = {
            "wait": (self._t("status_wait"), "#64748b"),
            "ok": (self._t("status_ok"), "#059669"),
            "fail": (self._t("status_fail"), "#dc2626"),
        }
        msg, color = status_map[self.auth_state]
        self.lbl_status.config(text=msg, fg=color)

        self.list_reviews.delete(0, tk.END)
        for r in t.reviews:
            self.list_reviews.insert(tk.END, f"{'★' * r.rating_stars}  {r.review_text}")

        s_cnt = len(t.seasons) if isinstance(t, TVShow) else 0
        self.lbl_stats.config(text=self._t("mem_stats").format(s=s_cnt, r=len(t.reviews), a=len(t.cast_actors)))

    def _log(self, msg: str):
        self.txt_log.config(state=tk.NORMAL)
        self.txt_log.insert(tk.END, msg + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state=tk.DISABLED)

    def _on_media_change(self):
        self.current_title = self.titles[self.media_var.get()]
        self.auth_state = "wait"
        self._refresh_views()

    def _handle_play(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ok = self.current_title.play_media(self.token_var.get().strip())
        if buf.getvalue().strip():
            self._log(buf.getvalue().strip())
        self.auth_state = "ok" if ok else "fail"
        self._refresh_views()

    def _handle_add_review(self):
        txt = self.entry_review.get().strip()
        if not txt:
            messagebox.showwarning(self._t("empty_warn_title"), self._t("empty_warn_msg"))
            return
        stars = int(self.rating_var.get())
        self.current_title.add_review(stars, txt)
        self.entry_review.delete(0, tk.END)
        self._log(self._t("log_review").format(stars=stars, name=self.current_title.name))
        self._refresh_views()

    def _handle_purge(self):
        if isinstance(self.current_title, TVShow):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.current_title.purge_tv_show_data()
            if buf.getvalue().strip():
                self._log(buf.getvalue().strip())
        else:
            self.current_title.reviews.clear()
            self._log(self._t("log_film_purge").format(name=self.current_title.name, a=len(self.current_title.cast_actors)))
        self._refresh_views()

    def _reset_all(self):
        self._init_data()
        self.media_var.set("Stranger Things (TVShow)")
        self.auth_state = "wait"
        self._log(self._t("log_reset"))
        self._refresh_views()


if __name__ == "__main__":
    root = tk.Tk()
    StreamyAppGUI(root)
    root.mainloop()