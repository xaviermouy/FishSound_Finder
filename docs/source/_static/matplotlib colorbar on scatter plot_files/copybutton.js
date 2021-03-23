const messages={'en':{'copy':'Copy','copy_to_clipboard':'Copy to clipboard','copy_success':'Copied!','copy_failure':'Failed to copy',},'es':{'copy':'Copiar','copy_to_clipboard':'Copiar al portapapeles','copy_success':'¡Copiado!','copy_failure':'Error al copiar',},'de':{'copy':'Kopieren','copy_to_clipboard':'In die Zwischenablage kopieren','copy_success':'Kopiert!','copy_failure':'Fehler beim Kopieren',}}
let locale='en'
if(document.documentElement.lang!==undefined&&messages[document.documentElement.lang]!==undefined){locale=document.documentElement.lang}
const runWhenDOMLoaded=cb=>{if(document.readyState!='loading'){cb()}else if(document.addEventListener){document.addEventListener('DOMContentLoaded',cb)}else{document.attachEvent('onreadystatechange',function(){if(document.readyState=='complete')cb()})}}
const codeCellId=index=>`codecell${index}`
const clearSelection=()=>{if(window.getSelection){window.getSelection().removeAllRanges()}else if(document.selection){document.selection.empty()}}
const temporarilyChangeTooltip=(el,newText)=>{const oldText=el.getAttribute('data-tooltip')
el.setAttribute('data-tooltip',newText)
setTimeout(()=>el.setAttribute('data-tooltip',oldText),2000)}
const addCopyButtonToCodeCells=()=>{if(window.ClipboardJS===undefined){setTimeout(addCopyButtonToCodeCells,250)
return}
const codeCells=document.querySelectorAll('div.highlight pre')
codeCells.forEach((codeCell,index)=>{const id=codeCellId(index)
codeCell.setAttribute('id',id)
const pre_bg=getComputedStyle(codeCell).backgroundColor;const clipboardButton=id=>`<a class="copybtn o-tooltip--left" style="background-color: ${pre_bg}" data-tooltip="${messages[locale]['copy']}" data-clipboard-target="#${id}">
      <img src="${DOCUMENTATION_OPTIONS.URL_ROOT}_static/copy-button.svg" alt="${messages[locale]['copy_to_clipboard']}">
    </a>`
codeCell.insertAdjacentHTML('afterend',clipboardButton(id))})
function escapeRegExp(string){return string.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');}
function formatCopyText(textContent,copybuttonPromptText,isRegexp=false,onlyCopyPromptLines=true,removePrompts=true){var regexp;var match;if(isRegexp){regexp=new RegExp('^('+copybuttonPromptText+')(.*)')}else{regexp=new RegExp('^('+escapeRegExp(copybuttonPromptText)+')(.*)')}
const outputLines=[];var promptFound=false;for(const line of textContent.split('\n')){match=line.match(regexp)
if(match){promptFound=true
if(removePrompts){outputLines.push(match[2])}else{outputLines.push(line)}}else{if(!onlyCopyPromptLines){outputLines.push(line)}}}
if(promptFound){textContent=outputLines.join('\n');}
if(textContent.endsWith("\n")){textContent=textContent.slice(0,-1)}
return textContent}
var copyTargetText=(trigger)=>{var target=document.querySelector(trigger.attributes['data-clipboard-target'].value);return formatCopyText(target.innerText,'',false,true,true)}
const clipboard=new ClipboardJS('.copybtn',{text:copyTargetText})
clipboard.on('success',event=>{clearSelection()
temporarilyChangeTooltip(event.trigger,messages[locale]['copy_success'])})
clipboard.on('error',event=>{temporarilyChangeTooltip(event.trigger,messages[locale]['copy_failure'])})}
runWhenDOMLoaded(addCopyButtonToCodeCells)