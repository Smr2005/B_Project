// Handle form submission via JS for dynamic result display
const form = document.getElementById("queryForm");
const resultsDiv = document.getElementById("result");

const escapeText = (value) => {
    if (value === undefined || value === null) {
        return "";
    }
    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
};

const formatSection = (title, icon, iconClass, body) => `
    <section class="results__section" style="--section-color: var(--${iconClass})">
        <div class="results__section-header">
            <i class="fas fa-${icon} ${iconClass}"></i>
            <h2>${title}</h2>
        </div>
        ${body}
    </section>
`;

// Create visual comparison diagram for queries
const createQueryComparisonDiagram = (originalQuery, optimizedQuery) => {
    const originalLines = originalQuery.split('\n').length;
    const optimizedLines = optimizedQuery.split('\n').length;
    const improvement = originalLines > optimizedLines ? 
        Math.round(((originalLines - optimizedLines) / originalLines) * 100) : 0;
    
    return `
        <div class="visual-comparison">
            <div class="comparison-cards">
                <div class="comparison-card comparison-card--before">
                    <div class="comparison-card__header">
                        <i class="fas fa-file-code"></i>
                        <span>BEFORE</span>
                    </div>
                    <div class="comparison-card__body">
                        <div class="metric">
                            <div class="metric__value">${originalLines}</div>
                            <div class="metric__label">Lines of Code</div>
                        </div>
                        <div class="status-indicator status-indicator--warning">
                            <i class="fas fa-exclamation-triangle"></i>
                            <span>Needs Optimization</span>
                        </div>
                    </div>
                </div>
                
                <div class="comparison-arrow">
                    <i class="fas fa-arrow-right"></i>
                    ${improvement > 0 ? `<span class="improvement-badge">-${improvement}%</span>` : ''}
                </div>
                
                <div class="comparison-card comparison-card--after">
                    <div class="comparison-card__header">
                        <i class="fas fa-check-circle"></i>
                        <span>AFTER</span>
                    </div>
                    <div class="comparison-card__body">
                        <div class="metric">
                            <div class="metric__value">${optimizedLines}</div>
                            <div class="metric__label">Lines of Code</div>
                        </div>
                        <div class="status-indicator status-indicator--success">
                            <i class="fas fa-check-circle"></i>
                            <span>Optimized</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
};

// Create visual performance metrics
const createPerformanceMetrics = (text) => {
    // Extract metrics from text
    const hasIndexOptimization = /index/i.test(text);
    const hasJoinOptimization = /join/i.test(text);
    const hasSubqueryOptimization = /subquery|derived table/i.test(text);
    const hasLimitOptimization = /limit/i.test(text);
    
    const metrics = [
        { label: 'Index Usage', icon: 'database', active: hasIndexOptimization, color: '#10b981' },
        { label: 'Join Optimization', icon: 'project-diagram', active: hasJoinOptimization, color: '#3b82f6' },
        { label: 'Subquery Handling', icon: 'layer-group', active: hasSubqueryOptimization, color: '#a855f7' },
        { label: 'Limit Optimization', icon: 'filter', active: hasLimitOptimization, color: '#f59e0b' }
    ];
    
    return `
        <div class="performance-metrics">
            <h4 class="metrics-title"><i class="fas fa-tachometer-alt"></i> Optimization Areas</h4>
            <div class="metrics-grid">
                ${metrics.map(m => `
                    <div class="metric-card ${m.active ? 'metric-card--active' : 'metric-card--inactive'}">
                        <div class="metric-card__icon" style="color: ${m.color}">
                            <i class="fas fa-${m.icon}"></i>
                        </div>
                        <div class="metric-card__label">${m.label}</div>
                        <div class="metric-card__status">
                            ${m.active ? 
                                '<i class="fas fa-check-circle" style="color: #10b981"></i>' : 
                                '<i class="fas fa-minus-circle" style="color: #6b7280"></i>'}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
};

// Create visual validation report with icons
const createValidationReport = (text) => {
    const sections = [];
    
    // Parse validation sections
    if (/syntax.*pass/i.test(text)) {
        sections.push({ title: 'Syntax Compliance', status: 'pass', icon: 'code' });
    } else if (/syntax.*fail/i.test(text)) {
        sections.push({ title: 'Syntax Compliance', status: 'fail', icon: 'code' });
    }
    
    if (/compatibility.*pass/i.test(text) || /compatible/i.test(text)) {
        sections.push({ title: 'MariaDB Compatibility', status: 'pass', icon: 'database' });
    } else if (/compatibility.*warning/i.test(text)) {
        sections.push({ title: 'MariaDB Compatibility', status: 'warning', icon: 'database' });
    }
    
    if (/safety.*pass/i.test(text) || /safe/i.test(text)) {
        sections.push({ title: 'Safety Assessment', status: 'pass', icon: 'shield-alt' });
    } else if (/safety.*warning/i.test(text) || /risk/i.test(text)) {
        sections.push({ title: 'Safety Assessment', status: 'warning', icon: 'shield-alt' });
    }
    
    if (/rewrite/i.test(text)) {
        sections.push({ title: 'Recommended Rewrites', status: 'info', icon: 'edit' });
    }
    
    const getStatusColor = (status) => {
        switch(status) {
            case 'pass': return '#10b981';
            case 'warning': return '#f59e0b';
            case 'fail': return '#ef4444';
            case 'info': return '#3b82f6';
            default: return '#6b7280';
        }
    };
    
    const getStatusIcon = (status) => {
        switch(status) {
            case 'pass': return 'check-circle';
            case 'warning': return 'exclamation-triangle';
            case 'fail': return 'times-circle';
            case 'info': return 'info-circle';
            default: return 'question-circle';
        }
    };
    
    return `
        <div class="validation-report">
            <div class="validation-grid">
                ${sections.map(s => `
                    <div class="validation-item validation-item--${s.status}">
                        <div class="validation-item__icon" style="color: ${getStatusColor(s.status)}">
                            <i class="fas fa-${s.icon}"></i>
                        </div>
                        <div class="validation-item__content">
                            <div class="validation-item__title">${s.title}</div>
                            <div class="validation-item__status">
                                <i class="fas fa-${getStatusIcon(s.status)}"></i>
                                <span>${s.status.toUpperCase()}</span>
                            </div>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
};

// Create visual cost analysis with charts
const createCostAnalysis = (text) => {
    // Extract cost-related information
    const hasSlowLog = /slow log/i.test(text);
    const hasStorage = /storage/i.test(text);
    const hasCaching = /cach/i.test(text);
    const hasIndex = /index/i.test(text);
    
    const items = [
        { label: 'Query Performance', icon: 'tachometer-alt', detected: hasSlowLog, impact: 'high' },
        { label: 'Storage Optimization', icon: 'hdd', detected: hasStorage, impact: 'medium' },
        { label: 'Caching Strategy', icon: 'memory', detected: hasCaching, impact: 'high' },
        { label: 'Index Efficiency', icon: 'sitemap', detected: hasIndex, impact: 'high' }
    ];
    
    const getImpactColor = (impact) => {
        switch(impact) {
            case 'high': return '#ef4444';
            case 'medium': return '#f59e0b';
            case 'low': return '#10b981';
            default: return '#6b7280';
        }
    };
    
    return `
        <div class="cost-analysis">
            <h4 class="metrics-title"><i class="fas fa-chart-bar"></i> Cost Optimization Opportunities</h4>
            <div class="cost-items">
                ${items.map(item => `
                    <div class="cost-item ${item.detected ? 'cost-item--detected' : ''}">
                        <div class="cost-item__header">
                            <div class="cost-item__icon">
                                <i class="fas fa-${item.icon}"></i>
                            </div>
                            <div class="cost-item__title">${item.label}</div>
                            <div class="cost-item__badge" style="background: ${getImpactColor(item.impact)}">
                                ${item.impact.toUpperCase()} IMPACT
                            </div>
                        </div>
                        <div class="cost-item__status">
                            ${item.detected ? 
                                '<i class="fas fa-exclamation-circle" style="color: #f59e0b"></i> <span>Optimization Available</span>' : 
                                '<i class="fas fa-check-circle" style="color: #10b981"></i> <span>Optimized</span>'}
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
};

// Create visual schema suggestions
const createSchemaSuggestions = (text) => {
    const suggestions = [];
    
    if (/index/i.test(text)) {
        suggestions.push({ 
            title: 'Indexing Strategy', 
            icon: 'sitemap', 
            color: '#3b82f6',
            description: 'Add or optimize indexes for better query performance'
        });
    }
    
    if (/data type/i.test(text)) {
        suggestions.push({ 
            title: 'Data Type Optimization', 
            icon: 'code', 
            color: '#10b981',
            description: 'Use appropriate data types to reduce storage'
        });
    }
    
    if (/partition/i.test(text)) {
        suggestions.push({ 
            title: 'Table Partitioning', 
            icon: 'th-large', 
            color: '#a855f7',
            description: 'Partition large tables for better manageability'
        });
    }
    
    if (/normaliz/i.test(text)) {
        suggestions.push({ 
            title: 'Data Modeling', 
            icon: 'project-diagram', 
            color: '#f59e0b',
            description: 'Review normalization and relationships'
        });
    }
    
    return `
        <div class="schema-suggestions">
            <div class="suggestions-grid">
                ${suggestions.map(s => `
                    <div class="suggestion-card">
                        <div class="suggestion-card__icon" style="background: ${s.color}">
                            <i class="fas fa-${s.icon}"></i>
                        </div>
                        <div class="suggestion-card__content">
                            <h5>${s.title}</h5>
                            <p>${s.description}</p>
                        </div>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
};

const formatSQLBlock = (label, content, icon = "file-code") => {
    const uniqueId = `sql-${Math.random().toString(36).substr(2, 9)}`;
    return `
    <div class="results__subsection">
        <div class="sql-header">
            <h3><i class="fas fa-${icon}"></i>${label}</h3>
            <button class="copy-btn" onclick="copyToClipboard('${uniqueId}')" title="Copy to clipboard">
                <i class="fas fa-copy"></i>
                <span>Copy</span>
            </button>
        </div>
        <div class="sql-code-wrapper">
            <pre class="sql-code" id="${uniqueId}"><code class="language-sql">${content}</code></pre>
        </div>
    </div>
`;};

const formatTextBlock = (content) => {
    // Check if content has bullet points
    if (content.includes('- ') || content.includes('• ')) {
        // Format bullet points with better styling
        const formatted = content
            .split('\n')
            .map(line => {
                if (line.trim().startsWith('- ') || line.trim().startsWith('• ')) {
                    return `<div class="bullet-item"><i class="fas fa-check-circle"></i>${line.replace(/^[\s-•]+/, '')}</div>`;
                }
                return line ? `<div class="text-line">${line}</div>` : '<div class="text-spacer"></div>';
            })
            .join('');
        return `<div class="bullet-list">${formatted}</div>`;
    }
    
    // Format regular text with better line breaks
    const formatted = content
        .split('\n')
        .map(line => line.trim() ? `<div class="text-line">${line}</div>` : '<div class="text-spacer"></div>')
        .join('');
    return `<div class="text-block">${formatted}</div>`;
};

const extractSQLFromResponse = (text) => {
    // Try to extract SQL from markdown code blocks
    const sqlMatch = text.match(/```sql\s*([\s\S]*?)\s*```/);
    if (sqlMatch) {
        return sqlMatch[1].trim();
    }
    
    // Try to extract from "Optimized SQL Query:" section
    const queryMatch = text.match(/Optimized SQL Query:\s*([\s\S]*?)(?=\n\n|Rationale:|$)/i);
    if (queryMatch) {
        return queryMatch[1].trim();
    }
    
    return text;
};

const extractRationaleFromResponse = (text) => {
    // Try to extract rationale section
    const rationaleMatch = text.match(/Rationale:\s*([\s\S]*?)$/i);
    if (rationaleMatch) {
        return rationaleMatch[1].trim();
    }
    return text;
};

const addStatusBadge = (text) => {
    // Add colored badges for status indicators
    text = text.replace(/\b(Pass|Success|Compatible|Safe)\b/gi, '<span class="badge badge-success">$1</span>');
    text = text.replace(/\b(Warning|Caution|Review)\b/gi, '<span class="badge badge-warning">$1</span>');
    text = text.replace(/\b(Error|Fail|Unsafe|Risk)\b/gi, '<span class="badge badge-error">$1</span>');
    text = text.replace(/\b(Info|Note|Recommended)\b/gi, '<span class="badge badge-info">$1</span>');
    return text;
};

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Show loading state
    resultsDiv.innerHTML = `
        <div class="loading">
            <i class="fas fa-spinner"></i>
            <p>Analyzing your query with AI agents...</p>
        </div>
    `;
    
    const formData = new FormData(form);

    try {
        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                sql_query: formData.get("query") || "",
            }),
        });

        const result = await response.json();

        if (!response.ok) {
            resultsDiv.innerHTML = `
                <div class="error">
                    <i class="fas fa-exclamation-circle"></i>
                    <span>Error: ${escapeText(result.detail || response.statusText)}</span>
                </div>
            `;
            return;
        }

        const {
            original_query: originalQuery,
            optimized_query: optimizedQuery,
            optimization_rationale: optimizationRationale,
            validation_report: validationReport,
            cost_estimation: costEstimation,
            schema_suggestions: schemaSuggestions,
        } = result;

        // Extract clean SQL from optimizer response
        const cleanOptimizedSQL = extractSQLFromResponse(optimizedQuery || "");
        const cleanRationale = extractRationaleFromResponse(optimizedQuery || "");

        // Build query comparison section with visual diagram
        const querySection = formatSection(
            "Query Comparison",
            "exchange-alt",
            "icon-queries",
            `
                ${createQueryComparisonDiagram(originalQuery || "", cleanOptimizedSQL || "")}
                ${formatSQLBlock("Original Query", escapeText(originalQuery || ""), "file-code")}
                ${formatSQLBlock("Optimized Query", escapeText(cleanOptimizedSQL || "(no changes)"), "check-circle")}
            `
        );

        // Build rationale section with performance metrics
        const rationaleText = cleanRationale || optimizationRationale || "(optimizer did not provide a rationale)";
        const rationaleSection = formatSection(
            "Optimization Rationale",
            "lightbulb",
            "icon-rationale",
            `
                ${createPerformanceMetrics(rationaleText)}
                ${formatTextBlock(escapeText(rationaleText))}
            `
        );

        // Build validation section with visual report
        const validationText = validationReport || "No validation report.";
        const validationSection = formatSection(
            "Data Validation Report",
            "shield-alt",
            "icon-validation",
            `
                ${createValidationReport(validationText)}
                ${formatTextBlock(addStatusBadge(escapeText(validationText)))}
            `
        );

        // Build cost estimation section with visual analysis
        const costText = costEstimation || "No cost estimation.";
        const costSection = formatSection(
            "Cost & Performance Analysis",
            "chart-line",
            "icon-cost",
            `
                ${createCostAnalysis(costText)}
                ${formatTextBlock(escapeText(costText))}
            `
        );

        // Build schema suggestions section with visual cards
        const schemaText = schemaSuggestions || "No schema suggestions.";
        const schemaSection = formatSection(
            "Schema Optimization Suggestions",
            "database",
            "icon-schema",
            `
                ${createSchemaSuggestions(schemaText)}
                ${formatTextBlock(escapeText(schemaText))}
            `
        );

        resultsDiv.innerHTML = `${querySection}${rationaleSection}${validationSection}${costSection}${schemaSection}`;
        
        // Apply syntax highlighting to all code blocks
        if (window.Prism) {
            Prism.highlightAll();
        }
        
        // Smooth scroll to results
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        
    } catch (err) {
        resultsDiv.innerHTML = `
            <div class="error">
                <i class="fas fa-exclamation-circle"></i>
                <span>Exception: ${escapeText(err.message || err)}</span>
            </div>
        `;
    }
});

// Copy to clipboard function
window.copyToClipboard = function(elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const text = element.textContent || element.innerText;
    
    // Use modern clipboard API
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopyFeedback(elementId);
        }).catch(err => {
            console.error('Failed to copy:', err);
            fallbackCopy(text);
        });
    } else {
        fallbackCopy(text);
    }
};

// Fallback copy method for older browsers
function fallbackCopy(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.select();
    
    try {
        document.execCommand('copy');
        showCopyFeedback();
    } catch (err) {
        console.error('Fallback copy failed:', err);
    }
    
    document.body.removeChild(textarea);
}

// Show visual feedback when copy is successful
function showCopyFeedback(elementId) {
    const button = document.querySelector(`button[onclick="copyToClipboard('${elementId}')"]`);
    if (!button) return;
    
    const originalHTML = button.innerHTML;
    button.innerHTML = '<i class="fas fa-check"></i><span>Copied!</span>';
    button.classList.add('copy-btn--success');
    
    setTimeout(() => {
        button.innerHTML = originalHTML;
        button.classList.remove('copy-btn--success');
    }, 2000);
}