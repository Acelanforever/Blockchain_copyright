// 页面加载动画
document.addEventListener('DOMContentLoaded', function() {
    document.body.classList.add('fade-in');
});

// 文件上传预览
function handleFileSelect(event) {
    const file = event.target.files[0];
    const fileSize = (file.size / 1024 / 1024).toFixed(2);
    
    if (fileSize > 16) {
        alert('文件大小不能超过16MB');
        event.target.value = '';
        return;
    }
    
    // 更新文件信息显示
    const fileInfo = document.getElementById('fileInfo');
    if (fileInfo) {
        fileInfo.textContent = `已选择: ${file.name} (${fileSize}MB)`;
    }
}

// 复制哈希值
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        showToast('复制成功！');
    }).catch(function(err) {
        showToast('复制失败，请手动复制');
    });
}

// 显示提示信息
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast show';
    toast.style.position = 'fixed';
    toast.style.bottom = '20px';
    toast.style.right = '20px';
    toast.style.backgroundColor = '#333';
    toast.style.color = '#fff';
    toast.style.padding = '10px 20px';
    toast.style.borderRadius = '4px';
    toast.style.zIndex = '1000';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// 表单验证
function validateForm() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value) {
                    isValid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                event.preventDefault();
                showToast('请填写所有必填字段');
            }
        });
    }
}

// 初始化所有功能
document.addEventListener('DOMContentLoaded', function() {
    // 初始化文件上传监听
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelect);
    }
    
    // 初��化表单验证
    validateForm();
    
    // 初始化复制按钮
    const copyButtons = document.querySelectorAll('.copy-btn');
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const text = this.getAttribute('data-copy');
            copyToClipboard(text);
        });
    });
});
