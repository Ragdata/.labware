# shellcheck shell=bash
# shellcheck disable=SC2155
####################################################################
# COMMON ELEMENTS
####################################################################
# License:      MIT License
# Repository:	https://github.com/Ragdata/.dotfiles
# Copyright:    Copyright © 2025 Redeyed Technologies
####################################################################
# TERMINAL FUNCTIONS
####################################################################
#
# FG COLORS
#
term::color::reset()	{ printf -- '%s0m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::black()					{ printf -- '%s30m' "$TERM_CSI"; }
term::red()						{ printf -- '%s31m' "$TERM_CSI"; }
term::green()					{ printf -- '%s32m' "$TERM_CSI"; }
term::gold()					{ printf -- '%s33m' "$TERM_CSI"; }
term::blue()					{ printf -- '%s34m' "$TERM_CSI"; }
term::magenta()				{ printf -- '%s35m' "$TERM_CSI"; }
term::cyan()					{ printf -- '%s36m' "$TERM_CSI"; }
term::lt_grey()				{ printf -- '%s37m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::grey()					{ printf -- '%s90m' "$TERM_CSI"; }
term::pink()					{ printf -- '%s91m' "$TERM_CSI"; }
term::lt_green()			{ printf -- '%s92m' "$TERM_CSI"; }
term::yellow()				{ printf -- '%s93m' "$TERM_CSI"; }
term::lt_blue()				{ printf -- '%s94m' "$TERM_CSI"; }
term::purple()				{ printf -- '%s95m' "$TERM_CSI"; }
term::lt_cyan()				{ printf -- '%s96m' "$TERM_CSI"; }
term::white()					{ printf -- '%s97m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::color()					{ printf -- '%s38;5;%sm' "$TERM_CSI" "$1"; }
term::rbg()						{ printf -- '%s38;2;%s;%s;%sm' "$TERM_CSI" "$1" "$2" "$3"; }
#
# BG COLORS
#
term::bg::reset()			{ printf -- '%s49m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::bg::black()			{ printf -- '%s40m' "$TERM_CSI"; }
term::bg::red()				{ printf -- '%s41m' "$TERM_CSI"; }
term::bg::green()			{ printf -- '%s42m' "$TERM_CSI"; }
term::bg::gold()			{ printf -- '%s43m' "$TERM_CSI"; }
term::bg::blue()			{ printf -- '%s44m' "$TERM_CSI"; }
term::bg::magenta()		{ printf -- '%s45m' "$TERM_CSI"; }
term::bg::cyan()			{ printf -- '%s46m' "$TERM_CSI"; }
term::bg::lt_grey()		{ printf -- '%s47m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::bg::grey()			{ printf -- '%s100m' "$TERM_CSI"; }
term::bg::pink()			{ printf -- '%s101m' "$TERM_CSI"; }
term::bg::lt_green()	{ printf -- '%s102m' "$TERM_CSI"; }
term::bg::yellow()		{ printf -- '%s103m' "$TERM_CSI"; }
term::bg::lt_blue()		{ printf -- '%s104m' "$TERM_CSI"; }
term::bg::purple()		{ printf -- '%s105m' "$TERM_CSI"; }
term::bg::lt_cyan()		{ printf -- '%s106m' "$TERM_CSI"; }
term::bg::white()			{ printf -- '%s107m' "$TERM_CSI"; }
# ------------------------------------------------------------------
term::bg::color()			{ printf -- '%s48;5;%sm' "$TERM_CSI" "$1"; }
term::bg::rbg()				{ printf -- '%s48;2;%s;%s;%sm' "$TERM_CSI" "$1" "$2" "$3"; }
#
# TEXT EFFECTS
#
term::blink()					{ printf -- '%s5m' "$TERM_CSI"; }
term::blink::rapid()	{ printf -- '%s6m' "$TERM_CSI"; }
term::no::blink()			{ printf -- '%s25m' "$TERM_CSI"; }
term::bold()					{ printf -- '%s1m' "$TERM_CSI"; }
term::dim()						{ printf -- '%s2m' "$TERM_CSI"; }
term::italic()				{ printf -- '%s3m' "$TERM_CSI"; }
term::normal()				{ printf -- '%s22m' "$TERM_CSI"; }
term::inverse()				{ printf -- '%s7m' "$TERM_CSI"; }
term::no::inverse()		{ printf -- '%s27m' "$TERM_CSI"; }
term::overline()			{ printf -- '%s53m' "$TERM_CSI"; }
term::no::overline()	{ printf -- '%s55m' "$TERM_CSI"; }
term::underline()			{ printf -- '%s4m' "$TERM_CSI"; }
term::underline::double()	{ printf -- '%s21m' "$TERM_CSI"; }
term::no::underline()	{ printf -- '%s24m' "$TERM_CSI"; }
term::underover()			{ printf -- '%s4;53m' "$TERM_CSI"; }
term::no::underover()	{ printf -- '%s24;55m' "$TERM_CSI"; }
term::invisible()			{ printf -- '%s8m' "$TERM_CSI"; }
term::visible()				{ printf -- '%s28m' "$TERM_CSI"; }
term::plain()					{ printf -- '%s23m' "$TERM_CSI"; }
term::strike()				{ printf -- '%s9m' "$TERM_CSI"; }
term::no::strike()		{ printf -- '%s29m' "$TERM_CSI"; }
####################################################################
# FUNCTION ALIASES
####################################################################
#
# FG ALIASES
#
export BLACK="$(term::black)"
export RED="$(term::red)"
export GREEN="$(term::green)"
export GOLD="$(term::gold)"
export BLUE="$(term::blue)"
export MAGENTA="$(term::magenta)"
export CYAN="$(term::cyan)"
export LT_GREY="$(term::lt_grey)"
export GREY="$(term::grey)"
export PINK="$(term::pink)"
export LT_GREEN="$(term::lt_green)"
export YELLOW="$(term::yellow)"
export LT_BLUE="$(term::lt_blue)"
export PURPLE="$(term::purple)"
export LT_CYAN="$(term::lt_cyan)"
export WHITE="$(term::white)"
# ------------------------------------------------------------------
export RESET="$(term::color::reset)"
export _0="$(term::color::reset)"
#
# BG ALIASES
#
export BG_BLACK="$(term::bg::black)"
export BG_RED="$(term::bg::red)"
export BG_GREEN="$(term::bg::green)"
export BG_GOLD="$(term::bg::gold)"
export BG_BLUE="$(term::bg::blue)"
export BG_MAGENTA="$(term::bg::magenta)"
export BG_CYAN="$(term::bg::cyan)"
export BG_LT_GREY="$(term::bg::lt_grey)"
export BG_GREY="$(term::bg::grey)"
export BG_PINK="$(term::bg::pink)"
export BG_LT_GREEN="$(term::bg::lt_green)"
export BG_YELLOW="$(term::bg::yellow)"
export BG_LT_BLUE="$(term::bg::lt_blue)"
export BG_PURPLE="$(term::bg::purple)"
export BG_LT_CYAN="$(term::bg::lt_cyan)"
export BG_WHITE="$(term::bg::white)"
# ------------------------------------------------------------------
export BG_RESET="$(term::bg::reset)"
export BG_0="$(term::bg::reset)"
#
# TEXT EFFECT ALIASES
#
export BLINK="$(term::blink)"
export BLINK_RAPID="$(term::blink::rapid)"
export NO_BLINK="$(term::no::blink)"
export BOLD="$(term::bold)"
export DIM="$(term::dim)"
export ITALIC="$(term::italic)"
export NORMAL="$(term::normal)"
export INVERSE="$(term::inverse)"
export NO_INVERSE="$(term::no::inverse)"
export OVERLINE="$(term::overline)"
export NO_OVERLINE="$(term::no::overline)"
export UNDERLINE="$(term::underline)"
export DOUBLE_UNDERLINE="$(term::underline::double)"
export NO_UNDERLINE="$(term::no::underline)"
export UNDEROVER="$(term::underover)"
export NO_UNDEROVER="$(term::no::underover)"
export INVISIBLE="$(term::invisible)"
export VISIBLE="$(term::visible)"
export PLAIN="$(term::plain)"
export STRIKE="$(term::strike)"
export NO_STRIKE="$(term::no::strike)"
#
# PRINTABLE
#
export DEFAULT_Y="[${WHITE}Y${_0}/n]"
export DEFAULT_N="[y/${WHITE}N${_0}]"
####################################################################
# FUNCTIONS
####################################################################
#
# echoAlias
#
echoAlias()
{
    (($# > 0)) || { echo -e "${RED}${SYMBOL_ERROR} echoAlias - At least one argument required${_0}"; exit 1; }

    local msg="$1"

    shift

    local COLOR="" PREFIX="" SUFFIX="" STREAM=1

    local OUTARGS=()

    options=$(getopt -l "color:,prefix:,suffix:,ERR,noline" -o "c:p:s:En" -a -- "$@")

    eval set --"$options"

    while true
    do
        case "$1" in
            -c | --color)
                COLOR="${2?}"
                OUTARGS+=("-e")
                shift 2
                ;;
            -p	| --prefix)
                PREFIX="${2?}"
                shift 2
                ;;
            -s | --suffix)
                SUFFIX="${2?}"
                shift 2
                ;;
            -E | --ERR)
                STREAM=2
                shift
                ;;
            -n | --noline)
                OUTARGS+=("-n")
                shift
                ;;
            --)
                shift
                break
                ;;
            *)
                echo -e "${RED}${SYMBOL_ERROR} echoAlias - Invalid Argument '$1'${RESET}"
                exit 1
                ;;
        esac
    done

    if [ "$msg" == "divider" ]; then
        msg="===================================================================="
    fi
    if [ "$msg" == "line" ]; then
        msg="--------------------------------------------------------------------"
    fi

    if [ -n "$COLOR" ]; then
        OUTPUT="${COLOR}${PREFIX}${msg}${SUFFIX}${_0}"
    else
        OUTPUT="${PREFIX}${msg}${SUFFIX}"
    fi

    if [[ "$STREAM" -eq 2 ]]; then
        echo "${OUTARGS[*]}" "${OUTPUT}" >&2
    else
        echo "${OUTARGS[*]}" "${OUTPUT}"
    fi
}
# ------------------------------------------------------------------
# TERMINAL COLOR ALIASES
# ------------------------------------------------------------------
echoBlack()			{ echoAlias "$1" -c "${BLACK}" "${@:2}"; }
echoRed()				{ echoAlias "$1" -c "${RED}" "${@:2}"; }
echoGreen()			{ echoAlias "$1" -c "${GREEN}" "${@:2}"; }
echoGold()			{ echoAlias "$1" -c "${GOLD}" "${@:2}"; }
echoBlue()			{ echoAlias "$1" -c "${BLUE}" "${@:2}"; }
echoMagenta()		{ echoAlias "$1" -c "${MAGENTA}" "${@:2}"; }
echoCyan()			{ echoAlias "$1" -c "${CYAN}" "${@:2}"; }
echoLtGrey()		{ echoAlias "$1" -c "${LT_GREY}" "${@:2}"; }
echoGrey()			{ echoAlias "$1" -c "${GREY}" "${@:2}"; }
echoPink()			{ echoAlias "$1" -c "${PINK}" "${@:2}"; }
echoLtGreen()		{ echoAlias "$1" -c "${LT_GREEN}" "${@:2}"; }
echoYellow()		{ echoAlias "$1" -c "${YELLOW}" "${@:2}"; }
echoLtBlue()		{ echoAlias "$1" -c "${LT_BLUE}" "${@:2}"; }
echoPurple()		{ echoAlias "$1" -c "${PURPLE}" "${@:2}"; }
echoLtCyan()		{ echoAlias "$1" -c "${LT_CYAN}" "${@:2}"; }
echoWhite()			{ echoAlias "$1" -c "${WHITE}" "${@:2}"; }
# ------------------------------------------------------------------
# TERMINAL STYLE ALIASES
# ------------------------------------------------------------------
echoDebug()			{ echoAlias "${ITALIC}$1${NORMAL}" -c "${WHITE}" "${@:2}"; }
echoDefault()		{ echoAlias "${RESET}$1" "${@:2}"; }
# ------------------------------------------------------------------
# TERMINAL MESSAGE ALIASES
# ------------------------------------------------------------------
echoError()			{ echoAlias "${SYMBOL_ERROR} $1" -c "${RED}" -E "${@:2}"; }
echoWarning()		{ echoAlias "${SYMBOL_WARNING} $1" -c "${GOLD}" "${@:2}"; }
echoInfo()			{ echoAlias "${SYMBOL_INFO} $1" -c "${LT_BLUE}" "${@:2}"; }
echoSuccess()		{ echoAlias "${SYMBOL_SUCCESS} $1" -c "${LT_GREEN}" "${@:2}"; }
echoTip()				{ echoAlias "${SYMBOL_TIP} $1" -c "${LT_BLUE}" "${@:2}"; }
echoImportant()	{ echoAlias "${SYMBOL_IMPORTANT} $1" -c "${LT_BLUE}" "${@:2}"; }
# ------------------------------------------------------------------
