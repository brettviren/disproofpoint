(defun disproofpoint ()
  (interactive)
  (save-excursion
    (let ((restr "\\(https://urldefense\.proofpoint\.com/v[[:digit:]]/url\\?u=\\)\\(.+?\\)\\(&[dcrms]=.*e=\\)")
          (inhibit-read-only t))
      (goto-char (point-min))
      (while (re-search-forward restr nil t)
        (let* ((url (match-string 2)))
          (replace-match
           (save-match-data
             (url-unhex-string
              (replace-regexp-in-string
               "_" "/"
               (replace-regexp-in-string
                "-" "%"
                url))))
           t t))))))

(provide 'disproofpoint)
