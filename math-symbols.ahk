#Requires AutoHotkey v2.0
#SingleInstance Force

WaitReleased(keyName) {
    if !keyName {
        return
    }

    try KeyWait keyName
}

WaitForHotstringKeys() {
    ; A_PriorKey catches the ending key for normal hotstrings and the final
    ; trigger key for immediate ones. The explicit keys cover common modifiers
    ; and editor-triggering keys which can make Ctrl+V land as another shortcut.
    WaitReleased A_PriorKey

    for keyName in ["Shift", "Ctrl", "Alt", "Space", "Enter", "Tab"] {
        WaitReleased keyName
    }
}

PasteText(text) {
    oldClipboard := ClipboardAll()

    A_Clipboard := ""
    A_Clipboard := text
    if !ClipWait(1) {
        A_Clipboard := oldClipboard
        return
    }

    WaitForHotstringKeys()
    Sleep 30
    SendInput "^v"
    Sleep 250
    A_Clipboard := oldClipboard
}

PasteSymbol(symbol) {
    PasteText symbol A_EndChar
}

PasteImmediate(symbol) {
    PasteText symbol
}

; CS40 math-symbol hotstrings.
; Type the trigger, then press Space/Enter/punctuation to replace it.
; Example: /neg Space -> ¬

; Logic
:X?:/neg::PasteSymbol "¬"
:X?:/not::PasteSymbol "¬"
:X?:/land::PasteSymbol "∧"
:X?:/and::PasteSymbol "∧"
:X?:/lor::PasteSymbol "∨"
:X?:/or::PasteSymbol "∨"
:X?:/xor::PasteSymbol "⊕"
:X?:/oplus::PasteSymbol "⊕"
:X?:/to::PasteSymbol "→"
:X?:/imp::PasteSymbol "⇒"
:X?:/implies::PasteSymbol "⇒"
:X?:/iff::PasteSymbol "↔"
:X?:/bicond::PasteSymbol "↔"
:X?:/equiv::PasteSymbol "≡"
:X?:/therefore::PasteSymbol "∴"
:X?:/because::PasteSymbol "∵"
:X?:/bot::PasteSymbol "⊥"
:X?:/top::PasteSymbol "⊤"
:X?:/models::PasteSymbol "⊨"
:X?:/vdash::PasteSymbol "⊢"

; Quantifiers
:X?:/forall::PasteSymbol "∀"
:X?:/fa::PasteSymbol "∀"
:X?:/exists::PasteSymbol "∃"
:X?:/ex::PasteSymbol "∃"
:X?:/nexists::PasteSymbol "∄"
:X?:/unique::PasteSymbol "∃!"

; Sets and membership
:X?:/in::PasteSymbol "∈"
:X?:/notin::PasteSymbol "∉"
:X?:/subset::PasteSymbol "⊂"
:X?:/subseteq::PasteSymbol "⊆"
:X?:/nsubseteq::PasteSymbol "⊈"
:X?:/supset::PasteSymbol "⊃"
:X?:/supseteq::PasteSymbol "⊇"
:X?:/cup::PasteSymbol "∪"
:X?:/union::PasteSymbol "∪"
:X?:/cap::PasteSymbol "∩"
:X?:/intersect::PasteSymbol "∩"
:X?:/setminus::PasteSymbol "∖"
:X?:/minus::PasteSymbol "∖"
:X?:/empty::PasteSymbol "∅"
:X?:/emptyset::PasteSymbol "∅"
:X?:/powerset::PasteSymbol "𝒫"
:X?:/pset::PasteSymbol "𝒫"
:X?:/comp::PasteSymbol "ᶜ"

; Relations, functions, and products
:X?:/times::PasteSymbol "×"
:X?:/cross::PasteSymbol "×"
:X?:/cart::PasteSymbol "×"
:X?:/circ::PasteSymbol "∘"
:X?:/compose::PasteSymbol "∘"
:X?:/mapsto::PasteSymbol "↦"
:X?:/maps::PasteSymbol "↦"
:X?:/dom::PasteSymbol "dom"
:X?:/ran::PasteSymbol "ran"
:X*?:/inv::PasteImmediate "⁻¹"
:X?:/degree::PasteSymbol "°"

; Comparison and arithmetic
:X?:/leq::PasteSymbol "≤"
:X?:/le::PasteSymbol "≤"
:X?:/geq::PasteSymbol "≥"
:X?:/ge::PasteSymbol "≥"
:X?:/neq::PasteSymbol "≠"
:X?:/ne::PasteSymbol "≠"
:X?:/approx::PasteSymbol "≈"
:X?:/sim::PasteSymbol "∼"
:X?:/propto::PasteSymbol "∝"
:X?:/pm::PasteSymbol "±"
:X?:/mp::PasteSymbol "∓"
:X?:/cdot::PasteSymbol "·"
:X?:/divides::PasteSymbol "∣"
:X?:/ndivides::PasteSymbol "∤"
:X?:/sqrt::PasteSymbol "√"
:X?:/inf::PasteSymbol "∞"

; Number systems and common constants
:X?:/N::PasteSymbol "ℕ"
:X?:/Z::PasteSymbol "ℤ"
:X?:/Q::PasteSymbol "ℚ"
:X?:/R::PasteSymbol "ℝ"
:X?:/C::PasteSymbol "ℂ"
:X?:/pi::PasteSymbol "π"
:X?:/theta::PasteSymbol "θ"
:X?:/alpha::PasteSymbol "α"
:X?:/beta::PasteSymbol "β"
:X?:/gamma::PasteSymbol "γ"
:X?:/delta::PasteSymbol "δ"
:X?:/epsilon::PasteSymbol "ε"
:X?:/lambda::PasteSymbol "λ"
:X?:/mu::PasteSymbol "μ"
:X?:/sigma::PasteSymbol "σ"
:X?:/Sigma::PasteSymbol "Σ"

; Arrows
:X?:/left::PasteSymbol "←"
:X?:/right::PasteSymbol "→"
:X?:/up::PasteSymbol "↑"
:X?:/down::PasteSymbol "↓"
:X?:/lra::PasteSymbol "↔"
:X?:/ra::PasteSymbol "→"
:X?:/la::PasteSymbol "←"
:X?:/Ra::PasteSymbol "⇒"
:X?:/La::PasteSymbol "⇐"
:X?:/LRa::PasteSymbol "⇔"

; Superscripts
; These use *? so they work immediately after symbols/letters, e.g. Z/^+ -> Z⁺.
; X + paste is more reliable in editors that do not accept injected Unicode keystrokes.
:X*?:/^0::PasteImmediate "⁰"
:X*?:/^1::PasteImmediate "¹"
:X*?:/^2::PasteImmediate "²"
:X*?:/^3::PasteImmediate "³"
:X*?:/^4::PasteImmediate "⁴"
:X*?:/^5::PasteImmediate "⁵"
:X*?:/^6::PasteImmediate "⁶"
:X*?:/^7::PasteImmediate "⁷"
:X*?:/^8::PasteImmediate "⁸"
:X*?:/^9::PasteImmediate "⁹"
:X*?:/^n::PasteImmediate "ⁿ"
:X*?:/^-::PasteImmediate "⁻"
:X*?:/^+::PasteImmediate "⁺"

; Subscripts
:X*?:/_0::PasteImmediate "₀"
:X*?:/_1::PasteImmediate "₁"
:X*?:/_2::PasteImmediate "₂"
:X*?:/_3::PasteImmediate "₃"
:X*?:/_4::PasteImmediate "₄"
:X*?:/_5::PasteImmediate "₅"
:X*?:/_6::PasteImmediate "₆"
:X*?:/_7::PasteImmediate "₇"
:X*?:/_8::PasteImmediate "₈"
:X*?:/_9::PasteImmediate "₉"
:X*?:/_n::PasteImmediate "ₙ"
:X*?:/_x::PasteImmediate "ₓ"
:X*?:/_i::PasteImmediate "ᵢ"
:X*?:/_j::PasteImmediate "ⱼ"
:X*?:/_k::PasteImmediate "ₖ"

; Quick proof words and templates
:X?:/pf::PasteSymbol "Proof."
:X?:/thm::PasteSymbol "Theorem."
:X?:/lem::PasteSymbol "Lemma."
:X?:/claim::PasteSymbol "Claim."
:X?:/qed::PasteSymbol "QED"
:X?:/st::PasteSymbol "such that"
:X?:/wlog::PasteSymbol "without loss of generality"
:X?:/contradiction::PasteSymbol "contradiction"
