class BlockchainVisualizer {
    constructor(containerId) {
        this.containerId = containerId;
        this.width = 1000;
        this.height = 200;
        this.blockWidth = 150;
        this.blockHeight = 100;
        this.initialize();
    }

    async initialize() {
        // 获取区块数据
        const response = await fetch('/blockchain/api/blocks');
        const blocks = await response.json();
        this.render(blocks);
    }

    render(blocks) {
        // 创建SVG容器
        const svg = d3.select(`#${this.containerId}`)
            .append('svg')
            .attr('width', this.width)
            .attr('height', this.height);

        // 创建区块组
        const blockGroups = svg.selectAll('g')
            .data(blocks)
            .enter()
            .append('g')
            .attr('transform', (d, i) => `translate(${i * (this.blockWidth + 50)}, 50)`);

        // 绘制区块
        blockGroups.append('rect')
            .attr('width', this.blockWidth)
            .attr('height', this.blockHeight)
            .attr('rx', 5)
            .attr('ry', 5)
            .style('fill', '#fff')
            .style('stroke', '#4a90e2')
            .style('stroke-width', 2);

        // 添加区块索引
        blockGroups.append('text')
            .attr('x', this.blockWidth / 2)
            .attr('y', 30)
            .attr('text-anchor', 'middle')
            .text(d => `Block #${d.index}`);

        // 添加连接箭头
        blockGroups.filter((d, i) => i > 0)
            .append('path')
            .attr('d', `M ${-30} ${this.blockHeight/2} L -10 ${this.blockHeight/2}`)
            .attr('stroke', '#4a90e2')
            .attr('stroke-width', 2)
            .attr('marker-end', 'url(#arrow)');

        // 添加箭头标记
        svg.append('defs').append('marker')
            .attr('id', 'arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 8)
            .attr('refY', 0)
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#4a90e2');
    }
}

// 初始化可视化
document.addEventListener('DOMContentLoaded', () => {
    new BlockchainVisualizer('blockchain-visualizer');
}); 