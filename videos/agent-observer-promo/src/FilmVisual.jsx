import React from 'react';
import {CardFrame, CardSurface, FilmBadge} from '../assets/fallback/primitives.jsx';

const base = {
  width: '100%', height: '100%', padding: 40, boxSizing: 'border-box',
  display: 'flex', flexDirection: 'column', gap: 18, justifyContent: 'center',
};

function Title({en, zh}) {
  return <div>
    <div style={{fontFamily: 'Georgia, serif', fontSize: 26, color: '#9CA3AF', letterSpacing: 4, textTransform: 'uppercase'}}>{en}</div>
    <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 44, fontWeight: 800, color: '#1C1917', marginTop: 6, lineHeight: 1.2}}>{zh}</div>
  </div>;
}

// 1) shot2 — CoreLoop：控制室图 + 流程链
export function CoreLoop({shot}) {
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, flexDirection: 'row', gap: 36, alignItems: 'center'}}>
      <div style={{flex: '0 0 38%', height: '70%', borderRadius: 12, overflow: 'hidden', boxShadow: '0 12px 32px rgba(15,26,46,0.25)'}}>
        <img src="/images/control-room.jpg" style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}} alt="巡天控制室"/>
      </div>
      <div style={{flex: 1, display: 'flex', flexDirection: 'column', gap: 14}}>
        <Title en="Agent decision loop" zh="每 15 分钟一个决策" />
        <div style={{display: 'flex', flexWrap: 'wrap', gap: 8}}>
          {['读取状态','理解局势','比较候选','做出观测决策','环境变化','再次决策'].map((s, i) => (
            <span key={i} data-enter="-1" style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 18, fontWeight: 600, padding: '6px 14px', borderRadius: 999, background: '#FEF2F2', color: '#991B1B', border: '1px solid #FECACA'}}>{s}</span>
          ))}
        </div>
      </div>
    </CardSurface>
  </CardFrame>;
}

// 2) shot3 — DecisionBadge：超大 900 秒数字徽章
export function DecisionBadge({shot}) {
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, alignItems: 'center', textAlign: 'center'}}>
      <FilmBadge>02 · 为什么让 AI 来做</FilmBadge>
      <div data-enter="-1" style={{fontFamily: 'Georgia, serif', fontSize: 220, fontWeight: 900, color: '#18242f', lineHeight: 1, letterSpacing: -4}}>900<tspan style={{fontSize: 80, marginLeft: 16, color: '#edb28b'}}>s</tspan></div>
      <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 32, color: '#374151', fontWeight: 600}}>= 15 分钟一次决策 · 一整夜持续推进</div>
      <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 20, color: '#9CA3AF'}}>不确定性 · 有限资源 · 多目标权衡 · 连续决策</div>
    </CardSurface>
  </CardFrame>;
}

// 3) shot4 — PrizeBoard：奖金数据卡组
export function PrizeBoard({shot}) {
  const tiles = [
    {tag: '🥇', name: '一等奖', count: '1', amount: '$2,000', color: '#DC2626'},
    {tag: '🥈', name: '二等奖', count: '2', amount: '$1,000', color: '#18242f'},
    {tag: '🥉', name: '三等奖', count: '3', amount: '$500', color: '#ed7b2f'},
  ];
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, alignItems: 'stretch'}}>
      <div style={{display: 'flex', alignItems: 'baseline', gap: 18, justifyContent: 'center'}}>
        <div style={{fontFamily: 'Georgia, serif', fontSize: 88, fontWeight: 900, color: '#DC2626', lineHeight: 1}}>$5,500</div>
        <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 28, fontWeight: 700, color: '#1C1917'}}>奖金池</div>
        <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 22, color: '#9CA3AF'}}>· 6 个现金奖项</div>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 18, marginTop: 12}}>
        {tiles.map((t, i) => (
          <div key={i} data-enter="-1" style={{background: '#FEF2F2', border: '1px solid #FEE2E2', borderRadius: 12, padding: 20, textAlign: 'center'}}>
            <div style={{fontSize: 36}}>{t.tag}</div>
            <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 18, color: '#9CA3AF', marginTop: 6}}>{t.name} · {t.count} 名</div>
            <div style={{fontFamily: 'Georgia, serif', fontSize: 38, fontWeight: 900, color: t.color, marginTop: 4}}>{t.amount}</div>
          </div>
        ))}
      </div>
    </CardSurface>
  </CardFrame>;
}

// 4) shot5 — AudienceList：5 类受众胶囊
export function AudienceList({shot}) {
  const groups = [
    {emoji: '🤖', tag: 'AI / Agent 开发者', desc: '把 Agent 从「聊天」推进到「连续决策」'},
    {emoji: '💻', tag: 'Python 开发者', desc: '从一个简单策略起步，不断提高分数'},
    {emoji: '🌌', tag: '天文 / AI for Science 爱好者', desc: '把科学问题变成 Agent 挑战'},
    {emoji: '🎓', tag: '学生与初学者', desc: '没有 Agent 经验也能参加'},
    {emoji: '🧠', tag: '喜欢复杂决策问题的人', desc: '「下一步到底怎么选」本身就值得挑战'},
  ];
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, gap: 12}}>
      {groups.map((g, i) => (
        <div key={i} data-enter="-1" style={{display: 'flex', alignItems: 'center', gap: 16, padding: '12px 18px', borderRadius: 999, background: '#FAFAF7', border: '1px solid #E5E7EB'}}>
          <span style={{fontSize: 32}}>{g.emoji}</span>
          <span style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 22, fontWeight: 700, color: '#1C1917', minWidth: 280}}>{g.tag}</span>
          <span style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 17, color: '#6B7280'}}>{g.desc}</span>
        </div>
      ))}
    </CardSurface>
  </CardFrame>;
}

// 5) shot6 — Requirements：你不需要 / 官方提供
export function Requirements({shot}) {
  const no = ['一台望远镜','天文专业背景','昂贵硬件','复杂本地基础设施'];
  const yes = ['巡天任务定义','模拟环境','开发工具包','公开开发场景','统一评测平台','线上培训','Python 3.12'];
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, flexDirection: 'row', gap: 28}}>
      <div style={{flex: 1, padding: 24, borderRadius: 12, background: '#FAFAF7', border: '1px solid #E5E7EB'}}>
        <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 20, fontWeight: 800, color: '#9CA3AF', marginBottom: 12}}>你不需要</div>
        {no.map((s, i) => (
          <div key={i} data-enter="-1" style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 20, color: '#9CA3AF', padding: '4px 0', textDecoration: 'line-through'}}>· {s}</div>
        ))}
      </div>
      <div style={{flex: 1, padding: 24, borderRadius: 12, background: '#FEF2F2', border: '1px solid #FEE2E2'}}>
        <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 20, fontWeight: 800, color: '#991B1B', marginBottom: 12}}>官方会提供</div>
        {yes.map((s, i) => (
          <div key={i} data-enter="-1" style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 19, color: '#1C1917', padding: '3px 0'}}>· {s}</div>
        ))}
      </div>
    </CardSurface>
  </CardFrame>;
}

// 6) shot7 — Schedule：3 段时间线
export function Schedule({shot}) {
  const items = [
    {emoji: '📚', date: '10/1–4', label: '线上培训', desc: '赛题讲解 · 工具包 · 入门指导'},
    {emoji: '⚔️', date: '10/5–7', label: '线上比赛', desc: '提交智能体 · 正式评测 · 排名'},
    {emoji: '🏆', date: '10/17', label: 'GOSIM 深圳颁奖', desc: '公布成绩 · 颁奖 · 全球开发者交流'},
  ];
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, gap: 18}}>
      {items.map((it, i) => (
        <div key={i} data-enter="-1" style={{display: 'flex', alignItems: 'center', gap: 20, padding: '14px 22px', borderRadius: 12, background: i === 1 ? '#FEF2F2' : '#FAFAF7', border: i === 1 ? '1px solid #FECACA' : '1px solid #E5E7EB'}}>
          <span style={{fontSize: 32}}>{it.emoji}</span>
          <span style={{fontFamily: 'Georgia, serif', fontSize: 30, fontWeight: 900, color: '#18242f', minWidth: 130}}>{it.date}</span>
          <span style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 24, fontWeight: 700, color: '#1C1917', minWidth: 180}}>{it.label}</span>
          <span style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 18, color: '#6B7280'}}>{it.desc}</span>
        </div>
      ))}
    </CardSurface>
  </CardFrame>;
}

// 7) shot8 — StartSteps：6 步流程
export function StartSteps({shot}) {
  const steps = [
    {n: '1', t: '报名', d: '注册比赛平台账号'},
    {n: '2', t: '建队', d: '1–8 人/队'},
    {n: '3', t: '下载工具包', d: '跑通官方基线'},
    {n: '4', t: '改你的策略', d: '从规则起步'},
    {n: '5', t: '提交评测', d: '提交到平台'},
    {n: '6', t: '看结果再改', d: '复盘 → 优化'},
  ];
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, gap: 12}}>
      <div style={{display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 16}}>
        {steps.map((s, i) => (
          <div key={i} data-enter="-1" style={{display: 'flex', alignItems: 'center', gap: 14, padding: '14px 18px', borderRadius: 12, background: '#FAFAF7', border: '1px solid #E5E7EB'}}>
            <span style={{display: 'inline-flex', alignItems: 'center', justifyContent: 'center', width: 44, height: 44, borderRadius: '50%', background: '#DC2626', color: '#fff', fontFamily: 'Georgia, serif', fontSize: 22, fontWeight: 900, flexShrink: 0}}>{s.n}</span>
            <div>
              <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 20, fontWeight: 700, color: '#1C1917'}}>{s.t}</div>
              <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 14, color: '#9CA3AF', marginTop: 2}}>{s.d}</div>
            </div>
          </div>
        ))}
      </div>
    </CardSurface>
  </CardFrame>;
}

// 8) shot9 — CTA：收尾图 + 链接
export function CTA({shot}) {
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, alignItems: 'center', gap: 14, background: 'linear-gradient(180deg,#0F1A2E 0%, #1a2a44 100%)', borderRadius: 12, color: '#fff'}}>
      <div style={{position: 'relative', width: '100%', height: '52%', borderRadius: 12, overflow: 'hidden'}}>
        <img src="/images/observatory-hero.jpg" style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block', opacity: 0.6}} alt="观测台"/>
      </div>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, padding: '14px 28px', borderRadius: 999, background: '#DC2626', boxShadow: '0 8px 24px rgba(220,38,38,0.45)'}}>
        <span style={{fontFamily: 'Georgia, serif', fontSize: 28, color: '#fff', fontWeight: 700, letterSpacing: 1}}>create.gosim.org</span>
        <span style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 22, color: '#fff', fontWeight: 600}}>/survey26/</span>
      </div>
      <div style={{fontFamily: '"PingFang SC","Noto Sans CJK SC",sans-serif', fontSize: 18, color: '#9CA3AF', letterSpacing: 1}}>现在就加入</div>
    </CardSurface>
  </CardFrame>;
}

// intro 镜头视觉（封面图 + 英文副标，让中文标题完全交给 copy）
export function HeroIntro({shot}) {
  return <CardFrame data-enter="-1">
    <CardSurface style={{...base, alignItems: 'center', textAlign: 'center', background: 'linear-gradient(180deg,#0F1A2E 0%, #18242f 100%)', borderRadius: 12, color: '#fff', gap: 14, maxHeight: '550px', overflow: 'hidden'}}>
      <div style={{position: 'relative', width: '90%', height: '440px', borderRadius: 12, overflow: 'hidden', boxShadow: '0 12px 40px rgba(0,0,0,0.4)'}}>
        <img src="/images/cover-strategy.jpg" style={{width: '100%', height: '100%', objectFit: 'cover', display: 'block'}} alt="观测智能体策略"/>
      </div>
      <div style={{fontFamily: 'Georgia, serif', fontSize: 22, color: '#edb28b', letterSpacing: 6, textTransform: 'uppercase'}}>What's next for the sky</div>
    </CardSurface>
  </CardFrame>;
}

// 路由表
export function VisualById({shot}) {
  switch (shot.component) {
    case 'FilmVisual/HeroIntro': return <HeroIntro shot={shot} />;
    case 'FilmVisual/CoreLoop': return <CoreLoop shot={shot} />;
    case 'FilmVisual/DecisionBadge': return <DecisionBadge shot={shot} />;
    case 'FilmVisual/PrizeBoard': return <PrizeBoard shot={shot} />;
    case 'FilmVisual/AudienceList': return <AudienceList shot={shot} />;
    case 'FilmVisual/Requirements': return <Requirements shot={shot} />;
    case 'FilmVisual/Schedule': return <Schedule shot={shot} />;
    case 'FilmVisual/StartSteps': return <StartSteps shot={shot} />;
    case 'FilmVisual/CTA': return <CTA shot={shot} />;
    default: return null;
  }
}
